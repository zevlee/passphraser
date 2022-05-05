#!/usr/bin/env python3

from secrets import choice, randbelow
from re import split
from os import mkdir, walk
from os.path import dirname, join, exists, expanduser
from shutil import copyfile
from platform import system
from json import loads, dumps
from gi import require_version
require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, GLib
from gi.repository.GdkPixbuf import Pixbuf


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
    version = open(join(dirname(__file__), "..", "VERSION")).read()


class Password:

    def __init__(self, lst, min, max, wrd, sep, cap, num, sym):
        # word list
        self.lst = split(r"\s+", open(lst, "r").read())
        # minimum word length
        self.min = min
        # maximum word length
        self.max = max
        # number of words
        self.wrd = wrd
        # separator
        self.sep = sep
        # capitalize
        self.cap = cap
        # add number
        self.num = num
        # add symbol
        self.sym = sym

    def _form_lexicon(self):
        """
        Forms lexicon from which words are chosen to create passwords
        """
        # filter self.lst based on length
        lexicon = []
        for word in self.lst:
            if len(word) >= self.min and len(word) <= self.max:
                lexicon.append(word)
        return lexicon

    def _form_sym_list(self):
        with open(join(Fn.conf_dir, "passphraser.json"), "r") as cfg:
            config = loads(cfg.read())
            cfg.close()
        symbols = []
        for symbol in Fn.symbols:
            if config[symbol]:
                symbols.append(symbol)
        sym_list = []
        for char in symbols:
            if char not in self.sep:
                sym_list.append(char)
        return sym_list

    def _add_num_sym(self, sym_list, num_ind, sym_ind, ind):
        result = ""
        if choice([True, False]):
            if self.num and ind == num_ind:
                num = str(randbelow(10))
                result += f"{num}{self.sep}"
            if self.sym and ind == sym_ind:
                try:
                    sym = choice(sym_list)
                except IndexError:
                    sym = ""
                result += f"{sym}{self.sep}"
        else:
            if self.sym and ind == sym_ind:
                try:
                    sym = choice(sym_list)
                except IndexError:
                    sym = ""
                result += f"{sym}{self.sep}"
            if self.num and ind == num_ind:
                num = str(randbelow(10))
                result += f"{num}{self.sep}"
        return result

    def password(self):
        """
        Creates password of `wrd` words from lexicon
        """
        lexicon = self._form_lexicon()
        sym_list = self._form_sym_list()

        result = ""
        # choose a random point to add a number
        num_ind = randbelow(self.wrd + 1)
        sym_ind = randbelow(self.wrd + 1)

        for i in range(self.wrd):
            # num and sym
            result += self._add_num_sym(sym_list, num_ind, sym_ind, i)
            # word
            word = choice(lexicon)
            if self.cap:
                result += f"{word.capitalize()}{self.sep}"
            else:
                result += f"{word.lower()}{self.sep}"
        # num and sym end case
        result += self._add_num_sym(sym_list, num_ind, sym_ind, self.wrd)
        if self.sep != "":
            result = result[:-len(self.sep)]
        return result, len(result)


class Header(Gtk.HeaderBar):

    def __init__(self, title, subtitle, version, application, window):
        Gtk.HeaderBar.__init__(self)
        self.title = title
        self.version = version
        self.app = application
        self.win = window
        self.set_title(self.title)
        self.set_subtitle(subtitle)
        self.set_show_close_button(True)

        # create menu
        action = Gio.SimpleAction.new("prefs", None)
        action.connect("activate", self.on_prefs)
        self.app.add_action(action)

        action = Gio.SimpleAction.new("reset", None)
        action.connect("activate", self.win.on_reset)
        self.app.add_action(action)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.app.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.app.on_quit)
        self.app.add_action(action)

        builder = Gtk.Builder.new_from_file(
            join(dirname(__file__), "..", "gui", "menu.xml")
        )
        menu = builder.get_object("app-menu")
        menu_button = Gtk.MenuButton.new()
        menu_button.set_image(
            Gtk.Image.new_from_icon_name(
                "emblem-system-symbolic",
                Gtk.IconSize.LARGE_TOOLBAR
            )
        )
        menu_button.set_menu_model(menu)
        # window decoration layout
        if system() == "Darwin":
            self.set_decoration_layout("close,minimize,maximize:")
            self.pack_start(menu_button)
        else:
            self.set_decoration_layout(":minimize,maximize,close")
            self.pack_end(menu_button)

    def on_prefs(self, action, param):
        """
        Open preferences window
        """
        prefs = Preferences()
        prefs.present()

    def on_about(self, action, param):
        """
        Open about dialog window
        """
        dialog = Gtk.AboutDialog(modal=True)
        dialog.set_position(Gtk.WindowPosition.CENTER)
        file = join(dirname(__file__), "..", "passphraser.svg")
        logo = Pixbuf.new_from_file(file)
        dialog.set_logo(logo)
        dialog.set_program_name(self.title)
        dialog.set_version(self.version)
        dialog.set_copyright("Copyright © 2021-2022 Zev Lee")
        license = open(join(dirname(__file__), "..", "LICENSE")).read()
        dialog.set_license(license)
        dialog.set_wrap_license(True)
        dialog.set_website("https://github.com/zevlee/passphraser")
        dialog.set_website_label("Homepage")
        dialog.present()


class Preferences(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_icon_from_file(
            join(dirname(__file__), "..", "passphraser.svg")
        )
        self.set_title("Preferences")
        self.set_border_width(40)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)
        self.set_modal(True)
        self.set_keep_above(True)

        # open stored preferences
        with open(join(Fn.conf_dir, "passphraser.json")) as cfg:
            self.config = loads(cfg.read())
            cfg.close()

        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        self.add(grid)
        grid.set_row_spacing(20)
        grid.set_column_spacing(20)

        # list of all symbols
        mode_label = Gtk.Label(halign=Gtk.Align.START)
        mode_label.set_markup("<b>Included Symbols</b>")
        grid.attach(mode_label, 0, 0, 4, 1)

        self.ti = Gtk.CheckButton(label="~")
        self.ti.set_active(self.config["~"])
        grid.attach(self.ti, 0, 1, 1, 1)

        self.gr = Gtk.CheckButton(label="`")
        self.gr.set_active(self.config["`"])
        grid.attach(self.gr, 1, 1, 1, 1)

        self.ex = Gtk.CheckButton(label="!")
        self.ex.set_active(self.config["!"])
        grid.attach(self.ex, 2, 1, 1, 1)

        self.at = Gtk.CheckButton(label="@")
        self.at.set_active(self.config["@"])
        grid.attach(self.at, 3, 1, 1, 1)

        self.po = Gtk.CheckButton(label="#")
        self.po.set_active(self.config["#"])
        grid.attach(self.po, 0, 2, 1, 1)

        self.do = Gtk.CheckButton(label="$")
        self.do.set_active(self.config["$"])
        grid.attach(self.do, 1, 2, 1, 1)

        self.pe = Gtk.CheckButton(label="%")
        self.pe.set_active(self.config["%"])
        grid.attach(self.pe, 2, 2, 1, 1)

        self.ca = Gtk.CheckButton(label="^")
        self.ca.set_active(self.config["^"])
        grid.attach(self.ca, 3, 2, 1, 1)

        self.am = Gtk.CheckButton(label="&")
        self.am.set_active(self.config["&"])
        grid.attach(self.am, 0, 3, 1, 1)

        self.ak = Gtk.CheckButton(label="*")
        self.ak.set_active(self.config["*"])
        grid.attach(self.ak, 1, 3, 1, 1)

        self.op = Gtk.CheckButton(label="(")
        self.op.set_active(self.config["("])
        grid.attach(self.op, 2, 3, 1, 1)

        self.cp = Gtk.CheckButton(label=")")
        self.cp.set_active(self.config[")"])
        grid.attach(self.cp, 3, 3, 1, 1)

        self.un = Gtk.CheckButton(label="_")
        self.un.set_active(self.config["_"])
        grid.attach(self.un, 0, 4, 1, 1)

        self.hy = Gtk.CheckButton(label="-")
        self.hy.set_active(self.config["-"])
        grid.attach(self.hy, 1, 4, 1, 1)

        self.pl = Gtk.CheckButton(label="+")
        self.pl.set_active(self.config["+"])
        grid.attach(self.pl, 2, 4, 1, 1)

        self.eq = Gtk.CheckButton(label="=")
        self.eq.set_active(self.config["="])
        grid.attach(self.eq, 3, 4, 1, 1)

        self.oc = Gtk.CheckButton(label="{")
        self.oc.set_active(self.config["{"])
        grid.attach(self.oc, 0, 5, 1, 1)

        self.ob = Gtk.CheckButton(label="[")
        self.ob.set_active(self.config["["])
        grid.attach(self.ob, 1, 5, 1, 1)

        self.cc = Gtk.CheckButton(label="}")
        self.cc.set_active(self.config["}"])
        grid.attach(self.cc, 2, 5, 1, 1)

        self.cb = Gtk.CheckButton(label="]")
        self.cb.set_active(self.config["]"])
        grid.attach(self.cb, 3, 5, 1, 1)

        self.vl = Gtk.CheckButton(label="|")
        self.vl.set_active(self.config["|"])
        grid.attach(self.vl, 0, 6, 1, 1)

        self.bs = Gtk.CheckButton(label="\\")
        self.bs.set_active(self.config["\\"])
        grid.attach(self.bs, 1, 6, 1, 1)

        self.co = Gtk.CheckButton(label=":")
        self.co.set_active(self.config[":"])
        grid.attach(self.co, 2, 6, 1, 1)

        self.sc = Gtk.CheckButton(label=";")
        self.sc.set_active(self.config[";"])
        grid.attach(self.sc, 3, 6, 1, 1)

        self.dq = Gtk.CheckButton(label="\"")
        self.dq.set_active(self.config["\""])
        grid.attach(self.dq, 0, 7, 1, 1)

        self.sq = Gtk.CheckButton(label="'")
        self.sq.set_active(self.config["'"])
        grid.attach(self.sq, 1, 7, 1, 1)

        self.lt = Gtk.CheckButton(label="<")
        self.lt.set_active(self.config["<"])
        grid.attach(self.lt, 2, 7, 1, 1)

        self.cm = Gtk.CheckButton(label=",")
        self.cm.set_active(self.config[","])
        grid.attach(self.cm, 3, 7, 1, 1)

        self.gt = Gtk.CheckButton(label=">")
        self.gt.set_active(self.config[">"])
        grid.attach(self.gt, 0, 8, 1, 1)

        self.pd = Gtk.CheckButton(label=".")
        self.pd.set_active(self.config["."])
        grid.attach(self.pd, 1, 8, 1, 1)

        self.qu = Gtk.CheckButton(label="?")
        self.qu.set_active(self.config["?"])
        grid.attach(self.qu, 2, 8, 1, 1)

        self.fs = Gtk.CheckButton(label="/")
        self.fs.set_active(self.config["/"])
        grid.attach(self.fs, 3, 8, 1, 1)

        self.sp = Gtk.CheckButton(label="(space)")
        self.sp.set_active(self.config[" "])
        grid.attach(self.sp, 0, 9, 1, 1)

        # all symbol options
        self.symbols = [
                self.ti, self.gr, self.ex, self.at,
                self.po, self.do, self.pe, self.ca,
                self.am, self.ak, self.op, self.cp,
                self.un, self.hy, self.pl, self.eq,
                self.oc, self.ob, self.cc, self.cb,
                self.vl, self.bs, self.co, self.sc,
                self.dq, self.sq, self.lt, self.cm,
                self.gt, self.pd, self.qu, self.fs,
                self.sp
        ]

        deselect_button = Gtk.Button(label="Deselect All")
        deselect_button.connect("clicked", self.on_deselect_clicked)
        grid.attach(deselect_button, 0, 10, 2, 1)

        select_button = Gtk.Button(label="Select All")
        select_button.connect("clicked", self.on_select_clicked)
        grid.attach(select_button, 2, 10, 2, 1)

        adv_label = Gtk.Label(halign=Gtk.Align.START)
        adv_label.set_markup("<b>Advanced</b>")
        grid.attach(adv_label, 0, 11, 4, 1)

        self.dbg = Gtk.CheckButton(label="Debug Mode")
        self.dbg.set_active(self.config["dbg"])
        grid.attach(self.dbg, 0, 12, 4, 1)

        cancel_button = Gtk.Button(label="Cancel")
        cancel_button.connect("clicked", self.on_cancel_clicked)
        grid.attach(cancel_button, 0, 13, 2, 1)

        select_button = Gtk.Button(label="Save")
        select_button.connect("clicked", self.on_save_clicked)
        grid.attach(select_button, 2, 13, 2, 1)

        self.show_all()

    def on_select_clicked(self, button):
        """
        Set all symbol options to true
        """
        for sym in self.symbols:
            sym.set_active(True)

    def on_deselect_clicked(self, button):
        """
        Set all symbol options to false
        """
        for sym in self.symbols:
            sym.set_active(False)

    def on_cancel_clicked(self, button):
        """
        Close preferences dialog without saving
        """
        self.destroy()

    def on_save_clicked(self, button):
        """
        Save preferences then close dialog
        """
        with open(join(Fn.conf_dir, "passphraser.json"), "w") as cfg:
            for k, v in zip(Fn.symbols, self.symbols):
                self.config[k] = v.get_active()
            self.config["dbg"] = self.dbg.get_active()
            cfg.write(dumps(self.config))
            cfg.close()
        self.destroy()


class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, application=app)
        self.app = app
        self.set_icon_from_file(
            join(dirname(__file__), "..", "passphraser.svg")
        )
        self.set_border_width(40)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(True)
        self.set_titlebar(
            Header(
                title="Passphraser",
                subtitle="Phrase-Based Password Generator",
                version="Version " + Fn.version,
                application=app,
                window=self
            )
        )

        with open(join(Fn.conf_dir, "passphraser.json"), "r") as cfg:
            self.config = loads(cfg.read())
            cfg.close()

        grid = Gtk.Grid()
        self.add(grid)
        grid.set_row_spacing(20)
        grid.set_column_spacing(20)

        lst_label = Gtk.Label(halign=Gtk.Align.START)
        lst_label.set_markup("<b>Word list</b>")
        grid.attach(lst_label, 0, 0, 1, 1)

        choose_list = Gtk.Button.new_with_mnemonic("_Choose Word List")
        choose_list.connect("clicked", self.on_file_clicked)
        grid.attach(choose_list, 1, 0, 1, 1)

        self.lst = Gtk.Entry()
        self.lst.set_text(self.config["lst"])
        grid.attach(self.lst, 0, 1, 2, 1)

        min_label = Gtk.Label(halign=Gtk.Align.START)
        min_label.set_markup("<b>Minimum word length</b>")
        grid.attach(min_label, 0, 2, 1, 1)

        self.min = Gtk.Entry()
        self.min.set_text(str(self.config["min"]))
        grid.attach(self.min, 1, 2, 1, 1)

        max_label = Gtk.Label(halign=Gtk.Align.START)
        max_label.set_markup("<b>Maximum word length</b>")
        grid.attach(max_label, 0, 3, 1, 1)

        self.max = Gtk.Entry()
        self.max.set_text(str(self.config["max"]))
        grid.attach(self.max, 1, 3, 1, 1)

        wrd_label = Gtk.Label(halign=Gtk.Align.START)
        wrd_label.set_markup("<b>Number of words</b>")
        grid.attach(wrd_label, 0, 4, 1, 1)

        self.wrd = Gtk.Entry()
        self.wrd.set_text(str(self.config["wrd"]))
        grid.attach(self.wrd, 1, 4, 1, 1)

        sep_label = Gtk.Label(halign=Gtk.Align.START)
        sep_label.set_markup("<b>Separator</b>")
        grid.attach(sep_label, 0, 5, 1, 1)

        self.sep = Gtk.Entry()
        self.sep.set_text(self.config["sep"])
        grid.attach(self.sep, 1, 5, 1, 1)

        self.cap = Gtk.CheckButton(label="Capitalize")
        self.cap.set_active(self.config["cap"])
        grid.attach(self.cap, 0, 6, 2, 1)

        self.num = Gtk.CheckButton(label="Add number")
        self.num.set_active(self.config["num"])
        grid.attach(self.num, 0, 7, 2, 1)

        self.sym = Gtk.CheckButton(label="Add symbol")
        self.sym.set_active(self.config["sym"])
        grid.attach(self.sym, 0, 8, 2, 1)

        gen_pwd = Gtk.Button(label="Generate Password")
        gen_pwd.connect("clicked", self.on_gen_pwd_clicked)
        grid.attach(gen_pwd, 0, 9, 2, 6)

        self.pwd_label = Gtk.Entry()
        self.pwd_label.set_editable(False)
        self.pwd_label.set_hexpand(True)
        self.pwd_label.set_vexpand(True)
        grid.attach(self.pwd_label, 0, 15, 2, 1)

        self.pwd_len = Gtk.Label(halign=Gtk.Align.START)
        grid.attach(self.pwd_len, 0, 16, 2, 1)

        self.show_all()

    def on_file_clicked(self, widget):
        """
        Open dialog to choose word list
        """
        dialog = Gtk.FileChooserDialog(
            title="Choose the word list",
            parent=None,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK,
        )
        dialog.set_current_folder(join(Fn.conf_dir, "wordlists"))
        dialog.set_position(Gtk.WindowPosition.CENTER)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file = dialog.get_filename()
            self.lst.set_text(file)
        dialog.destroy()

    def gen_pwd(self):
        """
        Gather parameters then generate the password
        """
        lst = self.lst.get_text()
        min = int(self.min.get_text())
        max = int(self.max.get_text())
        wrd = int(self.wrd.get_text())
        sep = self.sep.get_text()
        cap = self.cap.get_active()
        num = self.num.get_active()
        sym = self.sym.get_active()
        pwd = Password(lst, min, max, wrd, sep, cap, num, sym)
        gen_pwd, pwd_len = pwd.password()
        self.pwd_label.set_text(gen_pwd)
        self.pwd_len.set_text(f"Length: {str(pwd_len)}")
        with open(join(Fn.conf_dir, "passphraser.json"), "r") as cfg:
            self.config = loads(cfg.read())
            cfg.close()
        for k, v in zip(
            ["lst", "min", "max", "wrd", "sep", "cap", "num", "sym"],
            [lst, min, max, wrd, sep, cap, num, sym]
        ):
            self.config[k] = v
        with open(join(Fn.conf_dir, "passphraser.json"), "w") as cfg:
            cfg.write(dumps(self.config))
            cfg.close()

    def on_gen_pwd_clicked(self, button):
        """
        When generate password is clicked, call `gen_pwd`
        """
        config = loads(open(join(Fn.conf_dir, "passphraser.json"), "r").read())
        if not config["dbg"]:
            try:
                self.gen_pwd()
            except FileNotFoundError:
                dialog = Gtk.MessageDialog(
                    transient_for=None,
                    flags=0,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text="File not found"
                )
                dialog.set_position(Gtk.WindowPosition.CENTER)
                dialog.run()
                dialog.destroy()
            except Exception:
                dialog = Gtk.MessageDialog(
                    transient_for=None,
                    flags=0,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text="Invalid input"
                )
                dialog.set_position(Gtk.WindowPosition.CENTER)
                dialog.run()
                dialog.destroy()
        else:
            self.gen_pwd()

    def on_reset(self, action, param):
        """
        Reset fields to default parameters
        """
        for k, v in zip(
            ["lst", "min", "max", "wrd", "sep"],
            [self.lst, self.min, self.max, self.wrd, self.sep]
        ):
            v.set_text(str(self.app.dflt[k]))
        for k, v in zip(
            ["cap", "num", "sym"],
            [self.cap, self.num, self.sym]
        ):
            v.set_active(self.app.dflt[k])
        with open(join(Fn.conf_dir, "passphraser.json"), "w") as cfg:
            cfg.write(dumps(self.app.dflt))
            cfg.close()
        self.pwd_label.set_text("")
        self.pwd_len.set_text("")


class Application(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id="me.zevlee.Passphraser",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )
        GLib.set_application_name("Passphraser")

    def do_startup(self):
        Gtk.Application.do_startup(self)
        # default parameters
        self.dflt = {
            "lst": join(Fn.conf_dir, "wordlists", "eff_large.txt"),
            "min": 3,
            "max": 9,
            "wrd": 6,
            "sep": "-",
            "cap": True,
            "num": True,
            "sym": False,
            "dbg": False
        }
        for symbol in Fn.symbols:
            self.dflt[symbol] = True
        if not exists(Fn.conf_dir):
            mkdir(Fn.conf_dir)
        if not exists(join(Fn.conf_dir, "wordlists")):
            mkdir(join(Fn.conf_dir, "wordlists"))
            for subdir, dirs, files in walk(
                join(dirname(__file__), "..", "wordlists")
            ):
                for file in files:
                    copyfile(
                        join(subdir, file),
                        join(Fn.conf_dir, "wordlists", file)
                    )
        if not exists(join(Fn.conf_dir, "passphraser.json")):
            with open(join(Fn.conf_dir, "passphraser.json"), "w") as default:
                default.write(dumps(self.dflt))
                default.close()

    def do_activate(self):
        win = AppWindow(self)
        win.present()

    def on_quit(self, action, param):
        self.quit()
