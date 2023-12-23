from .metro_control import MetroControl
from ..label import Label


class MetroLabel(MetroControl, Label):

    from MetroFramework.Controls import MetroLabel

    _type = MetroLabel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)