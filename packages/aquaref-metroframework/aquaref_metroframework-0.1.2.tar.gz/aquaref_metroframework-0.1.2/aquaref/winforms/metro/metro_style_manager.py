from ...basic import Basic


class MetroStyleManager(Basic):

    from MetroFramework.Components import MetroStyleManager

    _type = MetroStyleManager

    def __init__(self):
        super().__init__()

    def GetOwner(self):
        return self.Owner

    def GetStyle(self):
        return self.Style

    def GetTheme(self):
        return self.Theme

    @property
    def Owner(self):
        return self._.Owner

    @Owner.setter
    def Owner(self, Window):
        self._.Owner = Window._

    def SetOwner(self, Window):
        self.Owner = Window

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

        self._.Style = getattr(MetroColorStyle, Color.capitalize())

    @property
    def Theme(self):
        return self._.Theme.ToString()

    @Theme.setter
    def Theme(self, Style: str):
        """
        主题

        Args:
            Color (str): 颜色样式可为：Black，Blue，Brown，Default，Green，Lime，Magenta，Orange，Pink，Purple，Red，Silver，Teal，White，Yellow
        """
        from MetroFramework import MetroThemeStyle

        if Style == "System":
            from darkdetect import isDark
            if isDark():
                self._.Theme = getattr(MetroThemeStyle, "Dark")
            else:
                self._.Theme = getattr(MetroThemeStyle, "Light")
            return

        self._.Theme = getattr(MetroThemeStyle, Style)
