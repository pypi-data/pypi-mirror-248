from ..base import NBase


class NTTheme(NBase):
    from TGUI import Theme

    _type = Theme

    def __init__(self, themepath):
        super().__init__(themepath)

    def renderer(self, id):
        from .exceptions import TGUIException
        try:
            return self._.getRenderer(id)
        except TGUIException:
            raise TGUIException("该主题暂不支持该组件")
