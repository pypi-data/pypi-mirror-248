from .metro_control import MetroControl
from ..button import Button


class MetroButton(MetroControl, Button):

    from MetroFramework.Controls import MetroButton

    _type = MetroButton

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)