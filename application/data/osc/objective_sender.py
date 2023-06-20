import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher

class ObjectiveOSCSender(DataEventDispatcher):

    #active = kp.BooleanProperty(True)

    teamID = kp.NumericProperty(0)
    buff_timer = kp.NumericProperty(0)
    source = kp.ObjectProperty()

    killer = kp.NumericProperty(0)

    state_path = kp.StringProperty()
    buff_timer_path = kp.StringProperty()
    killer_path = kp.StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.osc.setter('input_data'))


    def on_game_reset(self, *args):
        self.send_state()


    def on_source(self, *args):

        #self.source.bind(active=self.setter('active'))
        self.source.bind(buff_timer=self.setter('buff_timer'))
        self.source.bind(teamID=self.setter('teamID'))
        self.source.bind(killer=self.setter('killer'))


    def on_buff_timer(self, *args):
        self.send_state()


    def send_state(self, *args):

        team = int(self.teamID / 100)
        time = int(self.buff_timer / 1000)

        output = {
            f"{self.state_path}": team,
            f"{self.buff_timer_path}": time,
            f"{self.killer_path}": self.killer
        }

        self.send_data(**output)
