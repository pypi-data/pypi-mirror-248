from ..base import NBase


from SFML.Window import Styles

STYLE_CLOSE = Styles.Close
STYLE_DEFAULT = Styles.Default
STYLE_FULLSCREEN = Styles.Fullscreen
STYLE_NONE = getattr(Styles, "None")
STYLE_RESIZE = Styles.Resize
STYLE_TITLEBAR = Styles.Titlebar


class NTWindow(NBase):
    from SFML.Window import Window

    _type = Window

    def __init__(self, *args, width: int = 400, height: int = 300, title: str = "TGUI", style=STYLE_DEFAULT, **kwargs):
        from SFML.Window import VideoMode
        super().__init__(VideoMode(width, height), title, style)

        self.new_closed(self._close)

    def _close(self, s=None, e=None):
        self.close()

    def close(self):
        self._.Close()

    def dispatch_events(self):
        self._.DispatchEvents()

    def display(self):
        self._.Display()

    @property
    def isopen(self):
        return self._.IsOpen

    def mainloop(self):
        while self.isopen:
            self.dispatch_events()
            self.display()

    def new_closed(self, func):
        self._.Closed += lambda s, e: func(s, e)

    def remove_closed(self, func):
        self._.Closed -= func

    def title(self, text: str = None):
        if text:
            self._.SetTitle(text)