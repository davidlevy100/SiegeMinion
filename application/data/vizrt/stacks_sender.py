from datetime import datetime

import kivy.properties as kp

from data.events.data_event_dispatch import DataEventDispatcher

RelevantBuffs = {
    1680409346, # Kindred
    1467230133, # Draven
    3901057272, # Senna
    1960866709, # Veigar
    454914885, # Nasus
    2256731136, # Cho
    1721135316, # Bard
    3375836267, # Asol
    1911847746, # Sion
    2681101066, # Syndra
    2197950930, # Viktor
}

class StacksSender(DataEventDispatcher):

    current_stats_update = kp.DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(output=self.app.vizrt.setter('input_data'))
        self.app.livestats_history.bind(current_stats_update=self.setter('current_stats_update'))

    def on_game_reset(self, *args):
        output = {}
        self.app.vizrt.send_now(output)

    def on_current_stats_update(self, *args):
        output = {}
        if "participants" in self.current_stats_update and "gameTime" in self.current_stats_update:
            participant_list = self.current_stats_update["participants"]
            
            for participant in participant_list:
                stacks = "-1"
                if "stackingBuffs" in participant:
                    for buff in participant["stackingBuffs"]:
                        if buff["id"] in RelevantBuffs:
                            stacks = str(buff["stacks"])
                output[f"stacks/{participant['participantID']}"] = stacks

        print("sending output: ", output)
        self.send_data(**output)
        