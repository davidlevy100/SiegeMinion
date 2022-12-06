from pathlib import Path

import kivy.properties as kp
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle

from ui.constants.images import BARON_SOURCE, ELDER_SOURCE, DRAGON_SOURCE, TOWER_SOURCE, GOLD_SOURCE, KILL_SOURCE
from ui.constants.images import DRAGON_DEFAULT, DRAGON_CLOUD, DRAGON_INFERNAL, DRAGON_MOUNTAIN, DRAGON_OCEAN, DRAGON_CHEMTECH, DRAGON_HEXTECH
from ui.constants.images import BLUE_INHIB_SOURCE, RED_INHIB_SOURCE, INHIB_SOURCE

DRAGON_SOURCES = {
    "": DRAGON_DEFAULT,
    "default": DRAGON_DEFAULT,
    "fire": DRAGON_INFERNAL,
    "air": DRAGON_CLOUD,
    "water": DRAGON_OCEAN,
    "earth": DRAGON_MOUNTAIN,
    "elder": ELDER_SOURCE,
    "chemtech": DRAGON_CHEMTECH,
    "hextech": DRAGON_HEXTECH
}

class BaronImage(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.source = BARON_SOURCE


class ElderImage(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.source = ELDER_SOURCE


class DragonImage(Image):

    dragon_type = kp.OptionProperty(
        "default",
        options=[
            "",
            "default",
            "fire",
            "air",
            "water",
            "earth",
            "elder",
            "chemtech",
            "hextech"
        ]
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.source = DRAGON_DEFAULT

    
    def on_dragon_type(self, *args):

        self.source = DRAGON_SOURCES[self.dragon_type]


class TowerImage(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.source = TOWER_SOURCE


class GoldImage(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.source = GOLD_SOURCE


class KillImage(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.source = KILL_SOURCE


class BlueInhibImage(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.source = BLUE_INHIB_SOURCE


class RedInhibImage(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.source = RED_INHIB_SOURCE


class InhibImage(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.source = INHIB_SOURCE
