from json import dumps
from os import mkdir
from os.path import exists, join
from platform import system
from shutil import copytree

from gi import require_versions
require_versions({"Gtk": "4.0", "Adw": "1"})
from gi.repository import Gtk, Gdk, Gio, GLib, Adw

from . import *
from .window import Window


class Application(Adw.Application):
    """
    Application
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(
            application_id=ID,
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

        # Set application name
        GLib.set_application_name(APPNAME)

        # Set program name
        GLib.set_prgname(ID)

    def do_startup(self):
        """
        Start up application
        """
        Gtk.Application.do_startup(self)
        
        # Restore any missing files and folders
        if not exists(CONF):
            mkdir(CONF)
        if not exists(join(CONF, "wordlists")):
            copytree(
                join(APPDIR, "wordlists"),
                join(CONF, "wordlists")
            )
        if not exists(join(CONF, "settings.json")):
            with open(join(CONF, "settings.json"), "w") as s:
                default = read_config("default.json")
                s.write(dumps(default))
                s.close()
        if not exists(join(CONF, "default.json")):
            with open(join(CONF, "default.json"), "w") as d:
                d.write(dumps(DEFAULT))
                d.close()
        
        # Validate config files
        validate_config("default.json")
        validate_config("settings.json", "default.json")

        # Set color scheme
        appearance = read_config("settings.json")["app"]
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
                join(APPDIR, "usr", "share", "icons")
            )

    def do_activate(self):
        """
        Activate application
        """
        win = Window(self)
        win.show()
