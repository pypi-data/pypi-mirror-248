from .metro_control import MetroControl


class MetroPanel(MetroControl):

    from MetroFramework.Controls import MetroPanel

    _type = MetroPanel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)