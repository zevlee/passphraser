#!/usr/bin/env python3

from os.path import dirname, join, expanduser
from platform import system
from json import loads
from gi.repository import GLib


class Utils:

    # Application name
    NAME = "Passphraser"

    # Application ID
    ID = "me.zevlee.Passphraser"

    # Application directory
    APP_DIR = dirname(dirname(__file__))

    # Application version
    VERSION = open(join(APP_DIR, "VERSION")).read()

    # Config directory
    if system() == "Darwin":
        CONFIG_DIR = join(expanduser("~/Library/Application Support"), ID)
    else:
        CONFIG_DIR = join(GLib.get_user_config_dir(), NAME)

    # List of possible symbols to add to password
    SYMBOLS = [
        "~", "`", "!", "@", "#", "$",
        "%", "^", "&", "*", "(", ")",
        "_", "-", "+", "=", "{", "[",
        "}", "]", "|", "\\", ":", ";",
        "\"", "'", "<", ",", ">", ".",
        "?", "/", " "
    ]

    # Default parameters
    DEFAULT = {
        "lst": join(CONFIG_DIR, "wordlists", "eff_large.txt"),
        "min": 3,
        "max": 9,
        "wrd": 6,
        "sep": "-",
        "cap": True,
        "num": True,
        "sym": False,
        "app": True,
        "dbg": False
    }
    for symbol in SYMBOLS:
        DEFAULT[symbol] = True

    # Read config function
    @staticmethod
    def read_config(filename):
        """
        Given a file name `filename`, return the configuration dictionary or
        the default configuration if `filename` is not found
        """
        try:
            config = loads(open(join(Utils.CONFIG_DIR, filename), "r").read())
        except FileNotFoundError:
            config = Utils.DEFAULT
        return config
