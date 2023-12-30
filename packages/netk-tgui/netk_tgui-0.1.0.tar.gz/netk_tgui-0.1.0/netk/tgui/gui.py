from ..base import NBase


class NTGui(NBase):
    from TGUI import Gui

    _type = Gui

    from .renderwindow import NTRenderWindow

    def __init__(self, renderwindow: NTRenderWindow):
        super().__init__(renderwindow._)

    def add(self, widget: NBase):
        self._.Add(widget)

    def draw(self):
        self._.Draw()
