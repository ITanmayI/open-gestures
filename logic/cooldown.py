class Cooldown(object):
    def __init__(self):
        self.static = {
            "fist": 0.25,
            "open": 0.25,
            "2_finger": 2, #screenshot
            "3_finger": 2, #selfie
        },
        self.motion = {
            "swipe_left": 0.5,
            "swipe_right": 0.5,
            "swipe_up": 0.5,
            "swipe_down": 0.5,
        },
        self.directional = {
            "point_up": 0.1,
            "point_down": 0.1,
            "thumb_down": 0.1,
            "thumb_up": 0.1
        }