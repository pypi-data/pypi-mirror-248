from .metro_control import MetroControl


class MetroTabPage(MetroControl):

    from MetroFramework.Controls import MetroTabPage

    _type = MetroTabPage

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)