# pylint: disable=redefined-builtin
import json

from werkzeug import exceptions

# Notes on exceptions handling and errors:
# https://werkzeug.palletsprojects.com/en/master/exceptions/
# https://tools.ietf.org/html/rfc7807


class JSONException(exceptions.HTTPException):
    def get_headers(self, *args, **kwargs):
        """Get a list of headers."""
        return [("Content-Type", "application/json")]

    def get_body(self, *args, **kwargs):
        rv = {"status": int(self.code), "title": self.name}
        desc = self.get_description()
        if desc:
            rv["description"] = desc
        return json.dumps(rv, indent=4)

    def get_description(self, *args, **kwargs):
        return self.description


# 202 Accepted
class Accepted(JSONException):
    code = 202
    name = "Accepted"


# 204 No Content
class NoContent(JSONException):
    code = 204
    name = "No Content"


# 400 Bad Request
BadRequest = exceptions.BadRequest
# 401 Unauthorized
Unauthorized = exceptions.Unauthorized
# 403 Forbidden
Forbidden = exceptions.Forbidden
# 404 NotFound
NotFound = exceptions.NotFound
# 424 FailedDependency
FailedDependency = exceptions.FailedDependency

# 500 InternalServerError
InternalServerError = exceptions.InternalServerError

# 501 NotImplemented
NotImplemented = exceptions.NotImplemented

# 503 ServiceUnavailable
ServiceUnavailable = exceptions.ServiceUnavailable
