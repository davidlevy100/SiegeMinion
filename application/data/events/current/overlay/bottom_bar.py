from datetime import datetime

import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher


class BottomBar(DataEventDispatcher):

# Input Properties
    default_title = kp.StringProperty("")

    patch = kp.StringProperty("")

    date = kp.StringProperty("")

    current_title = kp.StringProperty()


    ## Damage Graph L3
    damage_bar_chart_l3_active = kp.BooleanProperty()
    damage_bar_chart_l3_title = kp.StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title_patch_date()

        self.app.config.add_callback(self.set_title_patch_date, "User Game Data")

        self.current_title = self.default_title


    def on_default_title(self, *args):

        self.current_title = self.default_title


    def set_info(self, date, patch, title, *args):

        self.date = date
        self.patch = patch
        self.default_title = title

        self.app.config.set("User Game Data", "default_title", title)
        self.app.config.set("User Game Data", "patch", patch)
        self.app.config.set("User Game Data", "date", date)

        self.app.config.write()

        self.update_now = str(datetime.now())


    def set_title_patch_date(self, *args):

        self.default_title = self.app.config.getdefault("User Game Data", "default_title", "")
        self.patch = self.app.config.getdefault("User Game Data", "patch", "")
        self.date = self.app.config.getdefault("User Game Data", "date", "")
