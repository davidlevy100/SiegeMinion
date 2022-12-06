import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher
from data.esports.stats import convert_milliseconds_to_HMS_string


class SpecialKillDispatcher(DataEventDispatcher):

    special_kill_event = kp.DictProperty()

    kill_type = kp.StringProperty("")
    killer = kp.NumericProperty(0)
    kill_streak_length = kp.NumericProperty(0)
    sequence_index = kp.NumericProperty(0)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.live_data.bind(special_kill_event=self.setter('special_kill_event'))


    def on_game_reset(self, *args):
        self.kill_type = ""
        self.killer = 0
        self.kill_streak_length = 0
        self.sequence_index = 0

        self.update()

        LogMessage = (
            f"Special Kill: has been reset"
        )
        Logger.info(LogMessage)


    def on_special_kill_event(self, *args):

        if (len(self.special_kill_event) > 0 and
            "killType" in self.special_kill_event and
            "killer" in self.special_kill_event and
            "gameTime" in self.special_kill_event and
            "sequenceIndex" in self.special_kill_event
        ):

            self.kill_type = self.special_kill_event["killType"]
            self.killer = self.special_kill_event["killer"]

            self.sequence_index = self.special_kill_event["sequenceIndex"]

            if "killStreakLength" in self.special_kill_event:
                self.kill_streak_length = self.special_kill_event["killStreakLength"]
            else:
                self.kill_streak_length = 0

            gametime = convert_milliseconds_to_HMS_string(self.special_kill_event["gameTime"])

            LogMessage = (
                f"Special Kill: {self.kill_type} of length {self.kill_streak_length} by participant #{self.killer} " 
                f"at gametime: {gametime}"
            )
            Logger.info(LogMessage)

        self.update()


    def update(self, *args):

        data = {
            "killType": self.kill_type,
            "killer": self.killer,
            "killStreakLength": self.kill_streak_length,
            "sequenceIndex": self.sequence_index
        }

        self.send_data(**data)
