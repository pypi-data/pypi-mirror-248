__all__ = []

import os

from connexion import request as current_request
from flask import current_app
from torxtools.pathtools import expandpath

from . import application

# TODO:
# - make it a configuration value
if os.geteuid() == 0:
    RD_WEBHOOKS_CACHEDIR = expandpath("/var/cache/rd-webhooks")
else:
    RD_WEBHOOKS_CACHEDIR = expandpath("$XDG_CACHE_HOME/rd-webhooks")


def build_query_string(params):
    if not params:
        return ""
    if isinstance(params, str):
        return params
    return "&".join("{}={}".format(k, v) for k, v in sorted(params.items()))
