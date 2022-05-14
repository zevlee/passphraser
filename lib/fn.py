#!/usr/bin/env python3

from os.path import join, expanduser
from platform import system
from gi.repository import GLib


class Fn:

    # config directory
    if system() == "Darwin":
        conf_dir = expanduser(
            "~/Library/Application Support/me.zevlee.Passphraser"
        )
    else:
        conf_dir = join(GLib.get_user_config_dir(), "Passphraser")
    # list of possible symbols to add to password
    symbols = [
        "~", "`", "!", "@",
        "#", "$", "%", "^",
        "&", "*", "(", ")",
        "_", "-", "+", "=",
        "{", "[", "}", "]",
        "|", "\\", ":", ";",
        "\"", "'", "<", ",",
        ">", ".", "?", "/",
        " "
    ]
    # application version
    version = open("VERSION").read()
