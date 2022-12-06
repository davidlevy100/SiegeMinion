#!/usr/bin/env python

from pathlib import Path

#placeholder for runes, items, champs, etc...
PLACEHOLDER_IMAGE = f"{Path().joinpath('ui', 'images', 'default', 'placeholder.png')}"

# Application Background
APP_BACKGROUND = f"{Path().joinpath('ui', 'images', 'background', 'champ-select-planning-intro.jpg')}"

## icons
ICON_PATH = Path().joinpath('ui', 'images', 'icon_images')
MONSTER_PATH = Path().joinpath('ui', 'images', 'monsters')

BARON_SOURCE = f"{ICON_PATH.joinpath('BaronIcon.png')}"
ELDER_SOURCE = f"{ICON_PATH.joinpath('ElderBuff.png')}"
DRAGON_SOURCE = f"{ICON_PATH.joinpath('dragon_minimap_icon_colorblind_128.png')}"
TOWER_SOURCE = f"{ICON_PATH.joinpath('icon_ui_tower_big.png')}"
GOLD_SOURCE = f"{ICON_PATH.joinpath('gold.png')}"
KILL_SOURCE = f"{ICON_PATH.joinpath('sword.png')}"

#DRAGONS
DRAGON_DEFAULT = f"{ICON_PATH.joinpath('dragon_default.png')}"
DRAGON_INFERNAL = f"{ICON_PATH.joinpath('FireBuff.png')}"
DRAGON_CLOUD = f"{ICON_PATH.joinpath('AirBuff.png')}"
DRAGON_MOUNTAIN = f"{ICON_PATH.joinpath('EarthBuff.png')}"
DRAGON_OCEAN = f"{ICON_PATH.joinpath('WaterBuff.png')}"
DRAGON_CHEMTECH = f"{ICON_PATH.joinpath('chemtech.png')}"
DRAGON_HEXTECH = f"{ICON_PATH.joinpath('hextech.png')}"

#INHIBITORS
BLUE_INHIB_SOURCE = f"{ICON_PATH.joinpath('inhibitor_building_100.png')}"
RED_INHIB_SOURCE = f"{ICON_PATH.joinpath('inhibitor_building_200.png')}"
INHIB_SOURCE = f"{ICON_PATH.joinpath('inhibitor.png')}"

#MISC
LOADING_IMG_PATH = f"{Path().joinpath('ui', 'images', 'default', 'image-loading.gif')}"
