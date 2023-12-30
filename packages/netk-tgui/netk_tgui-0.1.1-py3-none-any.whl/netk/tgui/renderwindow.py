from .window import NTWindow


class NTRenderWindow(NTWindow):
    from SFML.Graphics import RenderWindow

    _type = RenderWindow

    from .libs import path_tgui_libs_black_theme

    def __init__(self, *args, theme=path_tgui_libs_black_theme, **kwargs):
        super().__init__(*args, **kwargs)

        from .gui import NTGui
        from .theme import NTTheme

        self.gui = NTGui(self)
        self.theme = NTTheme(theme)

    def add(self, widget):
        self.gui.add(widget)

    def clear(self):
        self._.Clear()

    def mainloop(self):
        while self.isopen:
            self.dispatch_events()
            self.clear()
            self.gui.draw()
            self.display()

    def remove(self, widget):
        self.gui.remove(widget)