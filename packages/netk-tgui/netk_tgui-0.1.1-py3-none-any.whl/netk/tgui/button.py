from .widget import NTWidget


class NTButton(NTWidget):
    from TGUI import Button

    _type = Button
    id = "Button"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
