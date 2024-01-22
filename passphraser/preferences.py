#!/usr/bin/env python3

from . import Utils
from os.path import join
from shutil import copyfile
from platform import system
from json import dumps
from gi import require_versions
require_versions({"Gtk": "4.0", "Adw": "1"})
from gi.repository import Gtk, Adw


class Preferences(Gtk.Window):
    """
    Preferences window
    
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
            resizable=False,
            title="Preferences"
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

        # Included symbols label
        symbols_label = Gtk.Label(halign=Gtk.Align.START)
        symbols_label.set_markup("<b>Included Symbols</b>")

        # Symbol check buttons
        self.ti = Gtk.CheckButton(label="~")
        self.ti.set_active(self.config["~"])
        self.gr = Gtk.CheckButton(label="`")
        self.gr.set_active(self.config["`"])
        self.ex = Gtk.CheckButton(label="!")
        self.ex.set_active(self.config["!"])
        self.at = Gtk.CheckButton(label="@")
        self.at.set_active(self.config["@"])
        self.po = Gtk.CheckButton(label="#")
        self.po.set_active(self.config["#"])
        self.do = Gtk.CheckButton(label="$")
        self.do.set_active(self.config["$"])
        self.pe = Gtk.CheckButton(label="%")
        self.pe.set_active(self.config["%"])
        self.ca = Gtk.CheckButton(label="^")
        self.ca.set_active(self.config["^"])
        self.am = Gtk.CheckButton(label="&")
        self.am.set_active(self.config["&"])
        self.ak = Gtk.CheckButton(label="*")
        self.ak.set_active(self.config["*"])
        self.op = Gtk.CheckButton(label="(")
        self.op.set_active(self.config["("])
        self.cp = Gtk.CheckButton(label=")")
        self.cp.set_active(self.config[")"])
        self.un = Gtk.CheckButton(label="_")
        self.un.set_active(self.config["_"])
        self.hy = Gtk.CheckButton(label="-")
        self.hy.set_active(self.config["-"])
        self.pl = Gtk.CheckButton(label="+")
        self.pl.set_active(self.config["+"])
        self.eq = Gtk.CheckButton(label="=")
        self.eq.set_active(self.config["="])
        self.oc = Gtk.CheckButton(label="{")
        self.oc.set_active(self.config["{"])
        self.ob = Gtk.CheckButton(label="[")
        self.ob.set_active(self.config["["])
        self.cc = Gtk.CheckButton(label="}")
        self.cc.set_active(self.config["}"])
        self.cb = Gtk.CheckButton(label="]")
        self.cb.set_active(self.config["]"])
        self.vl = Gtk.CheckButton(label="|")
        self.vl.set_active(self.config["|"])
        self.bs = Gtk.CheckButton(label="\\")
        self.bs.set_active(self.config["\\"])
        self.co = Gtk.CheckButton(label=":")
        self.co.set_active(self.config[":"])
        self.sc = Gtk.CheckButton(label=";")
        self.sc.set_active(self.config[";"])
        self.dq = Gtk.CheckButton(label="\"")
        self.dq.set_active(self.config["\""])
        self.sq = Gtk.CheckButton(label="'")
        self.sq.set_active(self.config["'"])
        self.lt = Gtk.CheckButton(label="<")
        self.lt.set_active(self.config["<"])
        self.cm = Gtk.CheckButton(label=",")
        self.cm.set_active(self.config[","])
        self.gt = Gtk.CheckButton(label=">")
        self.gt.set_active(self.config[">"])
        self.pd = Gtk.CheckButton(label=".")
        self.pd.set_active(self.config["."])
        self.qu = Gtk.CheckButton(label="?")
        self.qu.set_active(self.config["?"])
        self.fs = Gtk.CheckButton(label="/")
        self.fs.set_active(self.config["/"])
        self.sp = Gtk.CheckButton(label="(space)")
        self.sp.set_active(self.config[" "])

        # Deselect all and select all buttons
        deselect_button = Gtk.Button(label="Deselect All")
        deselect_button.connect("clicked", self.on_deselect_clicked)
        select_button = Gtk.Button(label="Select All")
        select_button.connect("clicked", self.on_select_clicked)

        # Advanced label
        advanced_label = Gtk.Label(halign=Gtk.Align.START)
        advanced_label.set_markup("<b>Advanced</b>")

        # Appearance check button
        self.app = Gtk.CheckButton(label="Dark Mode")
        self.app.set_active(self.config["app"])

        # Debug mode check button
        self.dbg = Gtk.CheckButton(label="Debug Mode")
        self.dbg.set_active(self.config["dbg"])

        # Save settings as default check button
        self.default = Gtk.CheckButton(
            label="Save current settings as default"
        )

        # Cancel and save buttons
        cancel_button = Gtk.Button(label="Cancel")
        cancel_button.connect("clicked", self.on_cancel_clicked)
        save_button = Gtk.Button(label="Save")
        save_button.connect("clicked", self.on_save_clicked)

        # Attach widgets to grid
        symbols = [
            [self.ti, self.gr, self.ex, self.at, self.po, self.do],
            [self.pe, self.ca, self.am, self.ak, self.op, self.cp],
            [self.un, self.hy, self.pl, self.eq, self.oc, self.ob],
            [self.cc, self.cb, self.vl, self.bs, self.co, self.sc],
            [self.dq, self.sq, self.lt, self.cm, self.gt, self.pd],
            [self.qu, self.fs, self.sp]
        ]
        widgets = [[symbols_label]] + symbols + [
            [deselect_button, select_button],
            [advanced_label],
            [self.app],
            [self.dbg],
            [self.default],
            [cancel_button, save_button]
        ]
        for i in range(len(widgets)):
            width = max(len(row) for row in widgets) // len(widgets[i])
            for j in range(len(widgets[i])):
                if widgets[i] == symbols[-1]:
                    # Special case for last row of symbols
                    grid.attach(widgets[i][j], j, i, int(2 ** (j / 2)), 1)
                else:
                    grid.attach(widgets[i][j], j * width, i, width, 1)

        # Add grid
        self.set_child(grid)

        # Flattened list of symbol check buttons
        self.symbols = [symbol for row in symbols for symbol in row]

    def on_select_clicked(self, button):
        """
        Set all symbol check buttons to true
        
        :param button: Button
        :type button: Gtk.Button
        """
        for widget in self.symbols:
            widget.set_active(True)

    def on_deselect_clicked(self, button):
        """
        Set all symbol check buttons to false
        
        :param button: Button
        :type button: Gtk.Button
        """
        for widget in self.symbols:
            widget.set_active(False)

    def on_cancel_clicked(self, button):
        """
        Close preferences window without saving
        
        :param button: Button
        :type button: Gtk.Button
        """
        self.destroy()

    def on_save_clicked(self, button):
        """
        Save preferences then close dialog
        
        :param button: Button
        :type button: Gtk.Button
        """
        # Save preferences
        with open(join(CONF, "settings.json"), "w") as c:
            for k, v in zip(Utils.SYMBOLS, self.symbols):
                self.config[k] = v.get_active()
            self.config["app"] = self.app.get_active()
            self.config["dbg"] = self.dbg.get_active()
            c.write(dumps(self.config))
            c.close()
        # Set color scheme
        application = self.get_transient_for().get_application()
        if self.app.get_active():
            application.get_style_manager().set_color_scheme(
                Adw.ColorScheme.FORCE_DARK
            )
        else:
            application.get_style_manager().set_color_scheme(
                Adw.ColorScheme.FORCE_LIGHT
            )
        # Save settings to default
        if self.default.get_active():
            copyfile(
                join(CONF, "settings.json"),
                join(CONF, "default.json")
            )
        self.destroy()
