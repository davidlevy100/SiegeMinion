from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher


class DragonSoulEvent(DataEventDispatcher):

    dragon_soul_active = kp.BooleanProperty(False)
    dragon_soul = kp.StringProperty("default")
    dragon_soul_team = kp.NumericProperty(-1)

    active = kp.BooleanProperty(False)
    duration = kp.NumericProperty()
    run_event = None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.top_bar.bind(dragon_soul_active=self.setter('dragon_soul_active'))
        self.app.top_bar.bind(dragon_soul=self.setter('dragon_soul'))
        self.app.top_bar.bind(dragon_soul_team=self.setter('dragon_soul_team'))

        self.duration = self.app.config.get("User Game Data", "dragon_soul_duration")
        self.app.config.add_callback(self.set_duration, "User Game Data", "dragon_soul_duration")


    def on_game_reset(self, *args):
        self.active = False


    def on_active(self, *args):

        if self.run_event is not None:
            self.run_event.cancel()
            self.run_event = None

        if self.active: 
            self.run_event = Clock.schedule_once(self.deactivate, self.duration)

            LogMessage = (
                f"Dragon Soul Event: {datetime.now().strftime('%r')} "
                f"{self.dragon_soul} by team {self.dragon_soul_team}"
            )
            Logger.info(LogMessage)


    def activate(self, state, *args):

        if state == "down":
            self.active = True
        else:
            self.active = False


    def deactivate(self, *args):
        self.active = False

    def set_duration(self, *args):
        self.duration = float(args[-1])

    def set_name(self, *args):
        self.name = str(args[1])