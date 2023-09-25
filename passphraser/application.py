#!/usr/bin/env python3

from .utils import Utils
from .window import Window
from os import mkdir
from os.path import join, exists
from shutil import copytree
from platform import system
from json import dumps
from gi import require_versions
require_versions({"Gtk": "4.0", "Adw": "1"})
from gi.repository import Gtk, Gdk, Gio, GLib, Adw


class Application(Adw.Application):
    """
    Application
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(
            application_id=Utils.ID,
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

        # Set application name
        GLib.set_application_name(Utils.NAME)

        # Set program name
        GLib.set_prgname(Utils.ID)

    def do_startup(self):
        """
        Start up application
        """
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
        
        # Validate config files
        Utils.validate_config("default.json")
        Utils.validate_config("settings.json", "default.json")

        # Set color scheme
        appearance = Utils.read_config("settings.json")["app"]
        if appearance:
            self.get_style_manager().set_color_scheme(
                Adw.ColorScheme.FORCE_DARK
            )
        else:
            self.get_style_manager().set_color_scheme(
                Adw.ColorScheme.FORCE_LIGHT
            )

        # Set up icons for linux
        if system() == "Linux":
            icon_theme = Gtk.IconTheme.get_for_display(
                Gdk.Display.get_default()
            )
            icon_theme.add_search_path(
                join(Utils.APP_DIR, "usr", "share", "icons")
            )

    def do_activate(self):
        """
        Activate application
        """
        win = Window(self)
        win.show()
