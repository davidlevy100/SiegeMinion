import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher


class GameEndOSCSender(DataEventDispatcher):


    local_time = kp.NumericProperty(0)

    game_end_event = kp.DictProperty()

    nexus_taken = kp.NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.osc.setter('input_data'))

        self.app.livestats_history.bind(
            local_time=self.setter('local_time')
        )

        self.app.live_data.bind(game_end_event=self.setter('game_end_event'))


    def on_game_reset(self, *args):

        self.nexus_taken = 0

        self.send_state()


    def on_local_time(self, *args):

        self.send_time()

        if ("gameTime" in self.game_end_event and
            "winningTeam" in self.game_end_event and
            self.local_time >= self.game_end_event["gameTime"]
        ):
            self.nexus_taken = int(self.game_end_event["winningTeam"] / 100)

        else:

            self.nexus_taken = 0

        self.send_state()

    
    def send_state(self, *args):

        output = {
            "/NexusState/Taken": self.nexus_taken
        }

        self.send_data(**output)

    
    def send_time(self, *args):

        output = {
            "/GameState/Clock": int(self.local_time / 1000)
        }

        self.send_data(**output)
