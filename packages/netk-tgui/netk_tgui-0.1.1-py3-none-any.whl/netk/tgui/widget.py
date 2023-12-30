from ..base import NBase


from TGUI import AutoLayout

FILL = AutoLayout.Fill
TOP = AutoLayout.Top
BOTTOM = AutoLayout.Bottom
LEFT = AutoLayout.Left
RIGHT = AutoLayout.Right


from functools import singledispatch


class NTWidget(NBase):

    id = "Widget"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def pack(self, fill):
        self._.setAutoLayout(fill)

    def pos(self, x=None, y=None):
        if x or y:
            from SFML.System import Vector2f
            self._.Position = Vector2f(x, y)
        else:
            return self._.Position.X, self._.Position.Y

    from .renderwindow import NTRenderWindow
    from .theme import NTTheme

    def renderer(self, renderwindow: NTRenderWindow=None, theme: NTTheme=None, id=None):
        if id is None:
            id = self.id
        if renderwindow:
            theme = renderwindow.theme
        self._.SetRenderer(theme.renderer(id))

    def size(self, width=None, height=None):
        if width or height:
            from SFML.System import Vector2f
            self._.Size = Vector2f(width, height)
        else:
            return self._.Size.Width, self._.Size.Height

