#!/usr/bin/env python3

from lib.utils import Utils
from lib.password import Password
from lib.about import About
from lib.preferences import Preferences
from os.path import join
from shutil import copyfile
from platform import system
from json import dumps
from gi import require_versions
require_versions({"Gtk": "3.0"})
from gi.repository import Gtk, Gio


class Window(Gtk.ApplicationWindow):

    def __init__(self, app):
        super().__init__(
            application=app,
            resizable=True
        )

        # Add icon
        self.set_icon_name(Utils.ID)

        # Set up header
        header = Gtk.HeaderBar(title=Utils.NAME, show_close_button=True)

        # Build menu
        builder = Gtk.Builder.new_from_file(
            join(Utils.APP_DIR, "gui", "menu.xml")
        )
        menu = builder.get_object("app-menu")
        menu_button = Gtk.MenuButton()
        menu_button.set_image(
            Gtk.Image.new_from_icon_name(
                "open-menu-symbolic",
                Gtk.IconSize.SMALL_TOOLBAR
            )
        )
        menu_button.set_menu_model(menu)

        # Add menu actions
        action = Gio.SimpleAction.new("prefs", None)
        action.connect("activate", self.on_prefs_clicked)
        app.add_action(action)
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about_clicked)
        app.add_action(action)
        action = Gio.SimpleAction.new("reset", None)
        action.connect("activate", self.on_reset_clicked)
        app.add_action(action)

        # Set decoration layout
        if system() == "Darwin":
            header.set_decoration_layout("close,minimize,maximize:")
            header.pack_start(menu_button)
        else:
            header.set_decoration_layout(":minimize,maximize,close")
            header.pack_end(menu_button)

        # Add header
        self.set_titlebar(header)

        # Set up grid
        spacing = 20
        grid = Gtk.Grid(
            row_homogeneous=True,
            column_homogeneous=True,
            margin_start=spacing,
            margin_end=spacing,
            margin_top=spacing,
            margin_bottom=spacing,
            row_spacing=spacing,
            column_spacing=spacing
        )

        # Open stored preferences
        self.config = Utils.read_config("settings.json")

        # Word list label, button, and entry field
        lst_label = Gtk.Label(halign=Gtk.Align.START)
        lst_label.set_markup("<b>Word list</b>")
        lst_button = Gtk.Button.new_with_mnemonic("_Choose Word List")
        lst_button.connect("clicked", self.on_file_clicked)
        self.lst = Gtk.Entry()
        self.lst.set_text(self.config["lst"])

        # Minimum word length label and entry field
        min_label = Gtk.Label(halign=Gtk.Align.START)
        min_label.set_markup("<b>Minimum word length</b>")
        self.min = Gtk.Entry()
        self.min.set_text(str(self.config["min"]))

        # Maximum word length label and entry field
        max_label = Gtk.Label(halign=Gtk.Align.START)
        max_label.set_markup("<b>Maximum word length</b>")
        self.max = Gtk.Entry()
        self.max.set_text(str(self.config["max"]))

        # Number of words label and entry field
        wrd_label = Gtk.Label(halign=Gtk.Align.START)
        wrd_label.set_markup("<b>Number of words</b>")
        self.wrd = Gtk.Entry()
        self.wrd.set_text(str(self.config["wrd"]))

        # Separator label and entry field
        sep_label = Gtk.Label(halign=Gtk.Align.START)
        sep_label.set_markup("<b>Separator</b>")
        self.sep = Gtk.Entry()
        self.sep.set_text(self.config["sep"])

        # Capitalize words option
        self.cap = Gtk.CheckButton(label="Capitalize")
        self.cap.set_active(self.config["cap"])

        # Add number option
        self.num = Gtk.CheckButton(label="Add number")
        self.num.set_active(self.config["num"])

        # Add symbol option
        self.sym = Gtk.CheckButton(label="Add symbol")
        self.sym.set_active(self.config["sym"])

        # Generate password button
        generate = Gtk.Button(label="Generate Password")
        generate.connect("clicked", self.on_generate_clicked)

        # Generated password field
        self.password = Gtk.Entry()
        self.password.set_editable(False)
        self.password.set_hexpand(True)
        self.password.set_vexpand(True)

        # Password length
        self.password_length = Gtk.Label(halign=Gtk.Align.START)

        # Attach widgets to grid
        widgets = [
            [lst_label, lst_button],
            [self.lst],
            [min_label, self.min],
            [max_label, self.max],
            [wrd_label, self.wrd],
            [sep_label, self.sep],
            [self.cap],
            [self.num],
            [self.sym],
            [generate],
            [self.password],
            [self.password_length]
        ]
        for i in range(len(widgets)):
            width = max(len(row) for row in widgets) // len(widgets[i])
            for j in range(len(widgets[i])):
                grid.attach(widgets[i][j], j * width, i, width, 1)

        # Add grid
        self.add(grid)

        # Show all added widgets
        self.show_all()

    def on_prefs_clicked(self, action, param):
        """
        Open preferences window
        """
        prefs = Preferences(self)
        prefs.show()

    def on_about_clicked(self, action, param):
        """
        Open about dialog window
        """
        about = About(self)
        about.show()

    def on_reset_clicked(self, action, param):
        """
        Reset fields to default parameters
        """
        default = Utils.read_config("default.json")
        for k, v in zip(
            ["lst", "min", "max", "wrd", "sep"],
            [self.lst, self.min, self.max, self.wrd, self.sep]
        ):
            v.set_text(str(default[k]))
        for k, v in zip(
            ["cap", "num", "sym"],
            [self.cap, self.num, self.sym]
        ):
            v.set_active(default[k])
        self.password.set_text("")
        self.password_length.set_text("")
        copyfile(
            join(Utils.CONFIG_DIR, "default.json"),
            join(Utils.CONFIG_DIR, "settings.json")
        )

    def on_file_clicked(self, widget):
        """
        Open dialog to choose word list
        """
        dialog = Gtk.FileChooserDialog(
            title="Choose the word list",
            transient_for=self,
            modal=True,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            "_Cancel", Gtk.ResponseType.CANCEL,
            "_Open", Gtk.ResponseType.OK,
        )
        dialog.set_current_folder(join(Utils.CONFIG_DIR, "wordlists"))
        dialog.connect("response", self._select_file)
        dialog.show()

    def _select_file(self, dialog, response):
        """
        Set file when chosen in dialog
        """
        if response == Gtk.ResponseType.OK:
            self.lst.set_text(Gio.File.get_path(dialog.get_file()))
        dialog.destroy()

    def _generate_password(self):
        """
        Gather parameters then generate the password
        """
        # Open stored preferences
        self.config = Utils.read_config("settings.json")
        lst = self.lst.get_text()
        min = int(self.min.get_text())
        max = int(self.max.get_text())
        wrd = int(self.wrd.get_text())
        sep = self.sep.get_text()
        cap = self.cap.get_active()
        num = self.num.get_active()
        sym = self.sym.get_active()
        password = Password(
            lst, min, max, wrd, sep, cap, num, sym,
            self.config
        )
        generated = password.generate_password()
        self.password.set_text(generated)
        self.password_length.set_text(f"Length: {len(generated)}")
        # Save the settings used to generate the password
        for k, v in zip(
            ["lst", "min", "max", "wrd", "sep", "cap", "num", "sym"],
            [lst, min, max, wrd, sep, cap, num, sym]
        ):
            self.config[k] = v
        with open(join(Utils.CONFIG_DIR, "settings.json"), "w") as c:
            c.write(dumps(self.config))
            c.close()

    def on_generate_clicked(self, button):
        """
        Generate password when button is clicked
        """
        config = Utils.read_config("settings.json")
        if not config["dbg"]:
            dialog = Gtk.MessageDialog(
                transient_for=self,
                modal=True,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK
            )
            dialog.connect("response", self._confirm)
            try:
                self._generate_password()
            except FileNotFoundError:
                dialog.set_markup("File not found")
                dialog.show()
            except Exception:
                dialog.set_markup("Invalid input")
                dialog.show()
        else:
            self._generate_password()

    def _confirm(self, dialog, response):
        """
        Close upon confirming
        """
        dialog.destroy()
