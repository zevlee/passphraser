from gi import require_versions
require_versions({"Gdk": "4.0"})
from gi.repository import Gdk

from .application import Application


def main(argv):
    app = Application()
    app.run(argv)
