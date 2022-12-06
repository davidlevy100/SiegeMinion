import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher

class AllPlayersOSCSender(DataEventDispatcher):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.player1 = PlayerOSCSender(source=self.app.overlay_players.player1)
        self.player2 = PlayerOSCSender(source=self.app.overlay_players.player2)
        self.player3 = PlayerOSCSender(source=self.app.overlay_players.player3)
        self.player4 = PlayerOSCSender(source=self.app.overlay_players.player4)
        self.player5 = PlayerOSCSender(source=self.app.overlay_players.player5)
        self.player6 = PlayerOSCSender(source=self.app.overlay_players.player6)
        self.player7 = PlayerOSCSender(source=self.app.overlay_players.player7)
        self.player8 = PlayerOSCSender(source=self.app.overlay_players.player8)
        self.player9 = PlayerOSCSender(source=self.app.overlay_players.player9)
        self.player10 = PlayerOSCSender(source=self.app.overlay_players.player10)


class PlayerOSCSender(DataEventDispatcher):

    alive = kp.BooleanProperty(True)

    local_time = kp.NumericProperty(0)
    participant_ID = kp.NumericProperty()
    source = kp.ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.osc.setter('input_data'))

        self.app.livestats_history.bind(
            local_time=self.setter('local_time')
        )


    def on_alive(self, *args):

        output = {
            f"/PlayerState/Player{self.participant_ID}": int(self.alive)
        }

        self.send_data(**output)


    def on_local_time(self, *args):
        self.on_alive()


    def on_source(self, *args):
        self.source.bind(alive=self.setter('alive'))
        self.participant_ID = self.source.participant_ID
