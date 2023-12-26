from enum import Enum, unique

from attr import attrib, attrs
from flasket import endpoint
from gitlab import Gitlab

from rd_webhooks.clients import CommonClient
from rd_webhooks.exceptions import BadRequest, NoContent, ServiceUnavailable, Unauthorized
from rd_webhooks.utils.enums import StringMixin


@unique
class HTTPHeaders(StringMixin, Enum):
    X_GITLAB_EVENT = "X-Gitlab-Event"
    X_GITLAB_TOKEN = "X-Gitlab-Token"


@unique
class HookEvents(StringMixin, Enum):
    MERGE_REQUEST_HOOK = "Merge Request Hook"
    PIPELINE_HOOK = "Pipeline Hook"
    PUSH_HOOK = "Push Hook"
    SYSTEM_HOOK = "System Hook"
    TAG_PUSH_HOOK = "Tag Push Hook"


@unique
class SystemEvents(StringMixin, Enum):
    # List is synced with
    # - rd_webhooks/api/x-gitlab.yml
    # - https://docs.gitlab.com/ee/system_hooks/system_hooks.html
    PROJECT_CREATE = "project_create"
    PROJECT_DESTROY = "project_destroy"
    PROJECT_RENAME = "project_rename"
    PROJECT_TRANSfer = "project_transfer"
    PROJECT_UPDATE = "project_update"
    USER_ADD_TO_TEAM = "user_add_to_team"
    USER_REMOVE_FROM_TEAM = "user_remove_from_team"
    USER_UPDATE_FOR_TEAM = "user_update_for_team"
    USER_CREATE = "user_create"
    USER_DESTROY = "user_destroy"
    USER_FAILED_LOGIN = "user_failed_login"
    USER_RENAME = "user_rename"
    KEY_CREATE = "key_create"
    KEY_DESTROY = "key_destroy"
    GROUP_CREATE = "group_create"
    GROUP_DESTROY = "group_destroy"
    GROUP_RENAME = "group_rename"
    USER_ADD_TO_GROUP = "user_add_to_group"
    USER_REMOVE_FROM_GROUP = "user_remove_from_group"
    USER_UPDATE_FOR_GROUP = "user_update_for_group"

    @staticmethod
    def as_values():
        return [e.value for e in SystemEvents]


def webhook_endpoint(allowed_events):
    """
    Validate the X-Gitlab-Event against the value from decoratored function.

    TODO: use functools.wraps
    """

    def decorator(fn):
        @endpoint
        def wrapper(app, *args, **kwargs):
            headers = kwargs.pop("headers", app.request.headers)
            app.clients.gitlab.validate_webhook_token(headers)
            validate_webhook_event(headers, allowed_events)
            return fn(app=app, headers=headers, *args, **kwargs)

        return wrapper

    return decorator


def is_webhook_token_valid(header, cfgvalue):
    """
    Validate the X-Gitlab-Token against the value from the configuration file.

    If the configuration value is missing, None/Null, or True then
    authorization will always be denied.

    If the configuration value is False, then no validation will take place and
    authorization will always be allowed.

    :param header: value of "X-Gitlab-Token" from request headers
    :param cfgvalue: value of "x-gitlab-token" from configuration file
    :returns: True if authorized
    """
    if cfgvalue is None or cfgvalue is True:
        return False
    if cfgvalue is False:
        return True
    return cfgvalue == header


def validate_webhook_event(headers, allowed_events=None):
    """
    Validate the headers with X-Gitlab-Event against the allowed values with
    special provisions for the System Event hook that is recieved by all instance wide
    endpoints.

    If allowed_events is None: validation will take place against []
    If allowed_events is True: validation will always be successfull.
    If allowed_events is a list of HookEvents: validation will take place.

    :param headers: request headers
    :param allowed_events: None, True or list of HookEvents
    :raises: :class:`BadRequest`: Missing or invalid header
    :raises: :class:`NoContent`: System event accepted but ignored
    """
    if allowed_events is None:
        allowed_events = []
    if allowed_events is True:
        return

    current_event = headers.get(HTTPHeaders.X_GITLAB_EVENT.value)
    if current_event is None:
        raise BadRequest("Missing required header '%s'" % HTTPHeaders.X_GITLAB_EVENT)

    hook_event = None
    try:
        hook_event = HookEvents(current_event)
    except ValueError:
        raise BadRequest("Invalid required header '%s'" % HTTPHeaders.X_GITLAB_EVENT)

    if hook_event == HookEvents.SYSTEM_HOOK:
        if HookEvents.SYSTEM_HOOK not in allowed_events:
            raise NoContent

    if hook_event not in allowed_events:
        raise BadRequest("'%s' event is not handled by this endpoint" % current_event)


# ------------------------------------------------------------------------------
# Mixins
@attrs(kw_only=True)
class AttributeMixin:
    """
    Class that holds the attributes in __dict__
    """

    _attributes = attrib(factory=dict)

    def __attrs_post_init__(self):
        """
        Attributes passed at class creation are moved into self.__dict__
        """
        if self._attributes is not None:
            for k, v in self._attributes.items():
                self.__dict__[k] = v
            del self._attributes

    def __str__(self):
        return "{}({})".format(self.__class__.__name__, vars(self))


# ------------------------------------------------------------------------------
# Events
@attrs
class PushEvent(AttributeMixin):
    def __attrs_post_init__(self, *args, **kwargs):
        AttributeMixin.__attrs_post_init__(self)
        event_name = self.__dict__.get("event_name")
        assert event_name
        if event_name in SystemEvents.as_values():
            raise NoContent
        assert event_name in ["push", "tag_push"]

    def is_deletion(self):
        return self.after == "0000000000000000000000000000000000000000"

    def _ref_part(self, prefix):
        if not self.ref.startswith(prefix):
            return None
        return "/".join(self.ref.split("/")[2:])

    @property
    def ref_head(self):
        """return git reference without 'refs/heads/' part"""
        if self.object_kind != "push":
            return None
        return self._ref_part("refs/heads/")

    @property
    def ref_tag(self):
        """return git reference without 'refs/tags/' part"""
        if self.object_kind != "tag_push":
            return None
        return self._ref_part("refs/tags/")


# ------------------------------------------------------------------------------
class GitlabClient(CommonClient):
    def _connect(self):
        try:
            self.logger.info("GitLab: reading configuration...")
            host = self._config["host"]
            apikey = self._config["apikey"]
            # apikey is required as the first call after 'auth'
            # is a call to /user (current user)
            self.logger.info("GitLab: connecting to '%s'..." % host)
            rv = Gitlab(host, private_token=apikey)
            rv.auth()
            self.logger.info("GitLab: connection success.")
            return rv

        except BaseException as e:
            self.logger.info("GitLab: connection failure: %s" % e)
            raise ServiceUnavailable("GitLab auth failure")

    def validate_webhook_token(self, headers):
        """
            Validate the X-Gitlab-Token from headers against the value from the configuration file.

        :param headers: request headers
        :raises: :class:`Unauthorized`: Unauthorized
        :returns: nothing
        """
        if is_webhook_token_valid(
            headers.get(HTTPHeaders.X_GITLAB_TOKEN.value),
            self.config.get(HTTPHeaders.X_GITLAB_TOKEN.lower()),
        ):
            return
        raise Unauthorized("%s auth failure" % HTTPHeaders.X_GITLAB_TOKEN)
