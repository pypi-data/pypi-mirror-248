from .libs import libs
from ..core import NImport

tgui = NImport(libs["tgui.net.dll"])
SFML_Audio = NImport(libs["SFML.Audio.dll"])
SFML_Graphics = NImport(libs["SFML.Graphics.dll"])
SFML_System = NImport(libs["SFML.System.dll"])
SFML_Window = NImport(libs["SFML.Window.dll"])

from .gui import NTGui
from .renderwindow import NTRenderWindow
from .window import NTWindow, STYLE_CLOSE, STYLE_DEFAULT, STYLE_FULLSCREEN, STYLE_NONE, STYLE_RESIZE, STYLE_TITLEBAR