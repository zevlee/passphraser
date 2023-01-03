#!/usr/bin/env python3

from lib.utils import Utils
from os.path import join
from platform import system
from gi import require_versions
require_versions({"Gtk": "4.0", "Adw": "1"})
from gi.repository import Gtk


class About(Gtk.AboutDialog):
    """
    About dialog window

    :param parent: Parent window
    :type parent: Gtk.Window
    """
    def __init__(self, parent):
        """
        Constructor
        """
        super().__init__(
            modal=True,
            transient_for=parent,
            program_name=Utils.NAME,
            version=Utils.VERSION,
            copyright="Copyright © 2021-2023 Zev Lee",
            license_type=Gtk.License.MIT_X11,
            website="https://github.com/zevlee/passphraser",
            website_label="Homepage"
        )

        # Set up header
        header = Gtk.HeaderBar()

        # Set decoration layout
        if system() == "Darwin":
            header.set_decoration_layout("close,minimize,maximize:")
        else:
            header.set_decoration_layout(":minimize,maximize,close")

        # Add header
        self.set_titlebar(header)

        # Set up logo
        filename = join(Utils.APP_DIR, f"{Utils.ID}.svg")
        logo = Gtk.Image.new_from_file(filename)

        # Add logo
        self.set_logo(logo.get_paintable())
