from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.event import EventDispatcher
import kivy.properties as kp
from kivy.logger import Logger


class SponsorEvent(EventDispatcher):

    active = kp.BooleanProperty(False)
    section = kp.StringProperty("")
    prefix = kp.StringProperty("")
    sponsor_name = kp.StringProperty("")
    duration = kp.NumericProperty()
    run_event = None
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.sponsor_name = self.app.config.get(self.section, f"{self.prefix}_name")
        self.app.config.add_callback(self.set_name, self.section, f"{self.prefix}_name")

        self.duration = self.app.config.get(self.section, f"{self.prefix}_duration")
        self.app.config.add_callback(self.set_duration, self.section, f"{self.prefix}_duration")


    def on_game_reset(self, *args):
        self.active = False


    def on_active(self, *args):

        if self.run_event is not None:
            self.run_event.cancel()
            self.run_event = None

        if self.active: 
            self.run_event = Clock.schedule_once(self.deactivate, self.duration)

            LogMessage = (
                f"Sponsor Event: {datetime.now().strftime('%r')} "
                f"{self.sponsor_name}"
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
