""" /api/echo endpoint

files:
  rd_webhooks/api/echo.py
  rd_webhooks/api/echo.yml
"""

# pylint: disable=unused-argument, unused-import
from pprint import pprint

from flasket import endpoint


@endpoint
def post(*, app, headers, body, **_kwargs):
    return body
