from .metro_control import MetroControl


class MetroTabControl(MetroControl):

    from MetroFramework.Controls import MetroTabControl

    _type = MetroTabControl

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    from .metro_tab_page import MetroTabPage

    def CreatePage(self, Text: str = "") -> MetroTabPage:
        from .metro_tab_page import MetroTabPage
        _Page = MetroTabPage(self)
        _Page.Text = Text
        _Page.Pack(Dock="Fill")
        return _Page