from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
import kivy.properties as kp
from kivy.logger import Logger


from data.events.data_event_dispatch import DataEventDispatcher


class SpecialBaronAnnounceEvent(DataEventDispatcher):
    
    active = kp.BooleanProperty(False)
    disabled = kp.BooleanProperty(True)
    duration = kp.NumericProperty()
    run_event = None

    baron_stolen = kp.BooleanProperty(False)

    bpp_state = kp.OptionProperty(
        "spawning", 
        options=[
            "alive",
            "buff_active",
            "spawning",
            "respawning"
        ]
    )

    kill_type = kp.StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.duration = self.app.config.get("User Game Data", "special_baron_announce_duration")
        self.app.config.add_callback(self.set_duration, "User Game Data", "special_baron_announce_duration")

        self.bpp_state = self.app.baron_power_play.state
        self.app.baron_power_play.bind(state=self.setter('bpp_state'))

        self.kill_type = self.app.baron_power_play.kill_type
        self.app.baron_power_play.bind(kill_type=self.setter('kill_type'))

    def on_game_reset(self, *args):
        self.active = False
        self.disabled = True


    def on_active(self, *args):

        if self.run_event is not None:
            self.run_event.cancel()
            self.run_event = None

        if self.active: 
            self.run_event = Clock.schedule_once(self.deactivate, self.duration)

            LogMessage = (
                f"Special Baron Announce Event: {datetime.now().strftime('%r')} "
            )
            Logger.info(LogMessage)


    def on_bpp_state(self, *args):

        if self.bpp_state == "buff_active":
            self.disabled = False
        else:
            self.disabled = True


    def on_kill_type(self, *args):

        if self.kill_type == "steal":
            self.baron_stolen = True
        else:
            self.baron_stolen = False


    def activate(self, state, *args):

        if state == "down":
            self.active = True
        else:
            self.active = False


    def deactivate(self, *args):
        self.active = False

    def set_duration(self, *args):
        self.duration = float(args[-1])