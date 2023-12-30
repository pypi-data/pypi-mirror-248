from .window import NTWindow


class NTRenderWindow(NTWindow):
    from SFML.Graphics import RenderWindow

    _type = RenderWindow

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from .gui import NTGui

        self.gui = NTGui(self)

    def clear(self):
        self._.Clear()

    def mainloop(self):
        while self.isopen:
            self.dispatch_events()
            self.clear()
            self.gui.draw()
            self.display()