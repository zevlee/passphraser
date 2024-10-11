from os.path import dirname, join, expanduser
from platform import system
from json import loads, dumps
from gi.repository import GLib
from platformdirs import user_config_dir

# Application version
__version__ = "1.0.5"
# Application name
APPNAME = "Passphraser"
# Application ID
ID = "me.zevlee.Passphraser"
# Application directory
APPDIR = dirname(dirname(__file__))
# Config directory
CONF = user_config_dir(APPNAME)
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
    "lst": join(CONF, "wordlists", "eff_large.txt"),
    "mnw": 3,
    "mxw": 9,
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


def read_config(filename):
    """
    Given a filename `filename`, return the configuration dictionary or
    the default configuration if `filename` is not found
    
    :param filename: Filename
    :type filename: str
    :return: Configuration dictionary
    :rtype: dict
    """
    try:
        config = loads(open(join(CONF, filename), "r").read())
    except FileNotFoundError:
        config = DEFAULT
    return config


def validate_config(filename, default="RESET"):
    """
    Given a filename `filename`, replace the file with filename `default`
    if it is not valid
    
    :param filename: Config filename
    :type filename: str
    :param default: Default filename
    :type default: str
    """
    overwrite = False
    default_config = read_config(default)
    config = read_config(filename)
    # Remove invalid keys
    for key in [k for k in config.keys() if k not in DEFAULT.keys()]:
        config.pop(key)
        overwrite = True
    # Add missing keys
    for key in [k for k in DEFAULT.keys() if k not in config.keys()]:
        config[key] = default_config[key]
        overwrite = True
    # Validate config options
    for k in ["mnw", "mxw", "wrd", "cap", "num", "sym", "app", "dbg"]:
        if not isinstance(config[k], int):
            config[k] = default_config[k]
            overwrite = True
    # Overwrite filename if there is an error
    if overwrite:
        with open(join(CONF, filename), "w") as c:
            c.write(dumps(config))
            c.close()
