from ...basic import Basic


class MetroAnimationBase(Basic):

    from MetroFramework.Animation import AnimationBase

    _type = AnimationBase

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
