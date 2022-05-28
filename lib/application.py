#!/usr/bin/env python3

from lib.utils import Utils
from lib.window import Window
from os import mkdir
from os.path import join, exists
from shutil import copytree
from json import dumps
from gi import require_versions
require_versions({"Gtk": "3.0"})
from gi.repository import Gtk, Gio, GLib


class Application(Gtk.Application):

    def __init__(self):
        super().__init__(
            application_id=Utils.ID,
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

        # Set application name
        GLib.set_application_name(Utils.NAME)

        # Set program name
        GLib.set_prgname(Utils.ID)

    def do_startup(self):
        Gtk.Application.do_startup(self)

        # Restore any missing files and folders
        if not exists(Utils.CONFIG_DIR):
            mkdir(Utils.CONFIG_DIR)
        if not exists(join(Utils.CONFIG_DIR, "wordlists")):
            copytree(
                join(Utils.APP_DIR, "wordlists"),
                join(Utils.CONFIG_DIR, "wordlists")
            )
        if not exists(join(Utils.CONFIG_DIR, "settings.json")):
            with open(join(Utils.CONFIG_DIR, "settings.json"), "w") as s:
                default = Utils.read_config("default.json")
                s.write(dumps(default))
                s.close()
        if not exists(join(Utils.CONFIG_DIR, "default.json")):
            with open(join(Utils.CONFIG_DIR, "default.json"), "w") as d:
                d.write(dumps(Utils.DEFAULT))
                d.close()

    def do_activate(self):
        win = Window(self)
        win.show()
