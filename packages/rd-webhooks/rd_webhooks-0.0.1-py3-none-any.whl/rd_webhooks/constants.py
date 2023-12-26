import os

from boltons.iterutils import flatten_iter, unique_iter
from xdg import XDG_CONFIG_DIRS

DEFAULT_CONFIG_FILENAME = "rd-webhooks.yml"
# By not using expand here, the --help is clean of expanded vars
DEFAULT_CONFIG_SEARCH_PATHS = [
    # fmt: off
    e.format(DEFAULT_CONFIG_FILENAME) for e in unique_iter(
        flatten_iter(
            [
            "$XDG_CONFIG_HOME/{}",  # ~/.config/rd-webhooks.yml
            "~/.{}",                # ~/.rd-webhooks.yml
            [os.path.join(str(e), "{}") for e in XDG_CONFIG_DIRS],
            "/etc/{}",              # /etc/rd-webhooks.yml
            ],
        ),
    )
    # fmt: on
]

DEFAULT_SERVER_LISTEN = "localhost"
DEFAULT_SERVER_PORT = 8080

DEFAULT_CONFIGURATION = {
    "server": {
        "debug": False,
        "listen": DEFAULT_SERVER_LISTEN,
        "port": DEFAULT_SERVER_PORT,
        "ui": True,
        "workers": 0,
        "accesslog": "-",
        "errorlog": "-",
        "pidfile": None,
    },
    "gitlab": {
        "host": "https://gitlab.com",
        "apikey": None,
        "x-gitlab-token": None,
        "pages": "https://{group}.gitlab.io/{project}",
    },
}
