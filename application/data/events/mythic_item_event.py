from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
import kivy.properties as kp
from kivy.logger import Logger


from data.events.data_event_dispatch import DataEventDispatcher


class MythicItemEvent(DataEventDispatcher):

    accepting = kp.BooleanProperty(True)
    active = kp.BooleanProperty(False)
    disabled = kp.BooleanProperty(True)
    duration = kp.NumericProperty()
    run_event = None

    mythic_item = kp.DictProperty({})
    participant_ID = kp.NumericProperty()
    stat_time = kp.NumericProperty(0)
    team_ID = kp.NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.duration = self.app.config.get("User Game Data", "mythic_item_duration")
        self.app.config.add_callback(self.set_duration, "User Game Data", "mythic_item_duration")


    def on_game_reset(self, *args):
        self.active = False
        self.accepting = True
        self.disabled = True

        self.mythic_item.clear()
        self.participant_ID = 0
        self.stat_time = 0
        self.teamID = 0


    def on_active(self, *args):

        if self.run_event is not None:
            self.run_event.cancel()
            self.run_event = None

        if self.active: 
            self.run_event = Clock.schedule_once(self.deactivate, self.duration)

            LogMessage = (
                f"Mythic Item Event: {datetime.now().strftime('%r')} "
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


    def set_mythic_item(self, team_ID, participant_ID, item, time):

        if self.accepting:
            self.team_ID = team_ID
            self.participant_ID = participant_ID
            self.mythic_item = item
            self.accepting = False
            self.disabled = False
            self.stat_time = time
