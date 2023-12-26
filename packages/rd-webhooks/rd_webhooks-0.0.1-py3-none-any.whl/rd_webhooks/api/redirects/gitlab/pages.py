# """ /api/redirects/gitlab/* endpoint
#
# files:
#   rd_webhooks/api/redirects/gitlab/pages.py
#   rd_webhooks/api/redirects/gitlab/pages.yml
#   tests/api/redirects/gitlab/test_pages.py
# """


import flask
from flasket import endpoint

from rd_webhooks.models.badges import CachedBadge, StaticBadge


@endpoint
def get(*, app, group, path, template=None, **_kwargs):
    """/api/redirects/gitlab/pages/{group}/{path}"""
    if not template:
        template = app.config["gitlab"]["pages"]
    url = template.format(group=group, path=path)
    return flask.redirect(url, code=302)
