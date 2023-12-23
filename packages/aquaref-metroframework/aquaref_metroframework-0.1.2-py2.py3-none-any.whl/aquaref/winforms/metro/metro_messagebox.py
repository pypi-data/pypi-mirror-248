from .metro_form import MetroForm


class MetroMessageBox(MetroForm):
    from MetroFramework.Forms import MetroMessageBox

    _type = MetroMessageBox

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
