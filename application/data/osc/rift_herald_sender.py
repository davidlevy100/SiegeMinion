import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher


class RiftHeraldOSCSender(DataEventDispatcher):

    current_stats_update = kp.DictProperty()

    teamID = kp.NumericProperty(0)
    killerID = kp.NumericProperty(0)
    sequence_index = kp.NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.osc.setter('input_data'))

        self.app.livestats_history.bind(
            current_stats_update=self.setter('current_stats_update')
        )


    def on_current_stats_update(self, *args):

        if ("riftHerald" in self.current_stats_update and
            "killerTeamID" in self.current_stats_update["riftHerald"] and
            "killer" in self.current_stats_update["riftHerald"] and
            "sequenceIndex" in self.current_stats_update["riftHerald"]
        ):

            self.killerID = self.current_stats_update["riftHerald"]["killer"]
            self.teamID = self.current_stats_update["riftHerald"]["killerTeamID"]
            self.sequence_index = self.current_stats_update["riftHerald"]["sequenceIndex"]


    def on_sequence_index(self, *args):

        output = {
            "/RiftHeraldState/Team": self.teamID//100,
            "/RiftHeraldState/Killer":  self.killerID,
            "/RiftHeraldState/SequenceIndex": self.sequence_index
        }

        self.send_data(**output)
