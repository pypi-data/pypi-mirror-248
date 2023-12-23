from ...basic import Basic
from ..tooltip import ToolTip


class MetroToolTip(ToolTip, Basic):

    from MetroFramework.Components import MetroToolTip

    _type = MetroToolTip

    def __init__(self):
        super().__init__()
