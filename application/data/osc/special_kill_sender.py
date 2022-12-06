import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher


class SpecialKillOSCSender(DataEventDispatcher):

    current_stats_update = kp.DictProperty()
    
    kill_type = kp.StringProperty("")
    killer = kp.NumericProperty(0)
    kill_streak_length = kp.NumericProperty(0)
    sequence_index = kp.NumericProperty(0)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.osc.setter('input_data'))

        self.app.livestats_history.bind(
            current_stats_update=self.setter('current_stats_update')
        )


    def on_current_stats_update(self, *args):

        if ("champion_kill_special" in self.current_stats_update and
            "killType" in self.current_stats_update["champion_kill_special"] and
            "killer" in self.current_stats_update["champion_kill_special"] and
            "killStreakLength" in self.current_stats_update["champion_kill_special"] and
            "sequenceIndex" in self.current_stats_update["champion_kill_special"]
        ):

            self.kill_type = self.current_stats_update["champion_kill_special"]["killType"]
            self.killer = self.current_stats_update["champion_kill_special"]["killer"]
            self.kill_streak_length = self.current_stats_update["champion_kill_special"]["killStreakLength"]
            self.sequence_index = self.current_stats_update["champion_kill_special"]["sequenceIndex"]


    def on_sequence_index(self, *args):

        output = {
            "/SpecialKill/Type": self.kill_type,
            "/SpecialKill/Player":  self.killer,
            "/SpecialKill/StreakLength": self.kill_streak_length,
            "/SpecialKill/SequenceIndex": self.sequence_index
        }

        self.send_data(**output)
