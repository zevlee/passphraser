#!/usr/bin/env python3

from lib.utils import Utils
from os.path import join
from gi import require_versions
require_versions({"Gtk": "3.0"})
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf


class About(Gtk.AboutDialog):

    def __init__(self, parent):
        super().__init__(
            modal=True,
            transient_for=parent,
            program_name=Utils.NAME,
            version=Utils.VERSION,
            copyright="Copyright © 2021-2022 Zev Lee",
            license_type=Gtk.License.MIT_X11,
            website="https://github.com/zevlee/passphraser",
            website_label="Homepage"
        )

        # Set up logo
        filename = join(Utils.APP_DIR, f"{Utils.ID}.svg")
        logo = Pixbuf.new_from_file(filename)

        # Add logo
        self.set_logo(logo)
