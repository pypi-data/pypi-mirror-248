from .el_funcs import fixedrange, fixedindex
from .el_globs import globs
from .el_classes import pairs, component, game
from urllib.request import urlopen
import json

url = urlopen("https://raw.githubusercontent.com/endert1099/EndersUtils/main/versions.json")
versions = json.loads(url.read())

class EndersUtils():
    def __init__(self):
        self.fixedrange = fixedrange.fixedrange
        self.version = globs.LIBVERSION
        self.intversion = globs.LIBNUMVERSION
        self.pair = pairs.Pair
        self.fixedindex = fixedindex.fixedindex
        self.components = component.Components
        self.game = game.Game

# The main class used, although other instances can be made!
endersutils = EndersUtils()

if endersutils.intversion not in versions:
    raise ImportError(f"EndersUtils - Version {endersutils.intversion} is not up to date! Please use any of the following versions: {versions}")
