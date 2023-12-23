from ..control import Control


class MetroControl(Control):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def GetStyle(self):
        return self.Style

    def GetTheme(self):
        return self.Theme

    def SetStyle(self, Color: str):
        self.Style = Color

    def SetTheme(self, Style: str):
        self.Theme = Style

    @property
    def Style(self):
        """
        颜色样式
        """
        return self._.Style.ToString()

    @Style.setter
    def Style(self, Color: str):
        """
        颜色样式

        Args:
            Color (str): 颜色样式可为：Black，Blue，Brown，Default，Green，Lime，Magenta，Orange，Pink，Purple，Red，Silver，Teal，White，Yellow
        """

        from MetroFramework import MetroColorStyle

        self._.Style = getattr(MetroColorStyle, Color)

    @property
    def Theme(self):
        from MetroFramework import MetroThemeStyle

        return self._.Theme.ToString()

    @Theme.setter
    def Theme(self, Style: str):
        from MetroFramework import MetroThemeStyle, MetroColorStyle

        if Style == "System":
            from darkdetect import isDark
            if isDark():
                self._.Theme = getattr(MetroThemeStyle, "Dark")
            else:
                self._.Theme = getattr(MetroThemeStyle, "Light")
            return

        self._.Theme = getattr(MetroThemeStyle, Style)
