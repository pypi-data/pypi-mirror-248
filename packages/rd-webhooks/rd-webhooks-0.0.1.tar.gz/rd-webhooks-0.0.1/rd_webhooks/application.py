"""
Main R&D Webhooks application. It handles returning the WSGI application,
but also returning the potential services it can connect to and use.

On the OpenAPI side, it handles merging multiple yaml files into a single
specification before loading it.
"""

import logging
import os
import sys
import time
import uuid

from flasket import client

from rd_webhooks.clients.gitlab import GitlabClient


@client(name="gitlab")
def gitlab_client(*, app, name):
    cfg = app.config.get("gitlab", {})
    return GitlabClient(logger=logging.getLogger("stderr"), config=cfg)
