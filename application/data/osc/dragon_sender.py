import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher
from data.vizrt.viz_helper import get_dragon_code


class DragonOSCSender(DataEventDispatcher):

    current_stats_update = kp.DictProperty()

    sequence_index = kp.NumericProperty(0)

    dragon_left_1 = kp.StringProperty("default")
    dragon_left_2 = kp.StringProperty("default")
    dragon_left_3 = kp.StringProperty("default")
    dragon_left_4 = kp.StringProperty("default")

    dragon_right_1 = kp.StringProperty("default")
    dragon_right_2 = kp.StringProperty("default")
    dragon_right_3 = kp.StringProperty("default")
    dragon_right_4 = kp.StringProperty("default")

    dragon_team = kp.NumericProperty(0)
    dragon_killed = kp.NumericProperty(0)

    dragon_soul_team = kp.NumericProperty(0)
    dragon_soul = kp.NumericProperty(0)

    last_dragon_killer = kp.NumericProperty(0)
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.osc.setter('input_data'))

        self.app.livestats_history.bind(
            current_stats_update=self.setter('current_stats_update')
        )

        self.app.top_bar.bind(dragon_left_1=self.setter('dragon_left_1'))
        self.app.top_bar.bind(dragon_left_2=self.setter('dragon_left_2'))
        self.app.top_bar.bind(dragon_left_3=self.setter('dragon_left_3'))
        self.app.top_bar.bind(dragon_left_4=self.setter('dragon_left_4'))

        self.app.top_bar.bind(dragon_right_1=self.setter('dragon_right_1'))
        self.app.top_bar.bind(dragon_right_2=self.setter('dragon_right_2'))
        self.app.top_bar.bind(dragon_right_3=self.setter('dragon_right_3'))
        self.app.top_bar.bind(dragon_right_4=self.setter('dragon_right_4'))

        self.app.top_bar.bind(last_dragon_killer=self.setter('last_dragon_killer'))


    def on_current_stats_update(self, *args):

        if "sequenceIndex" in self.current_stats_update:
            self.sequence_index = self.current_stats_update["sequenceIndex"]


    def on_game_reset(self, *args):

        self.sequence_index = 0
        self.dragon_team = 0
        self.dragon_killed = 0
        self.dragon_soul_team = 0
        self.dragon_soul = 0

        self.send_dragon_state()
        self.send_dragon_soul_state()
        


    def on_last_dragon_killer(self, *args):

        if self.last_dragon_killer == 0:
            self.dragon_team = 0
        elif self.last_dragon_killer < 6:
            self.dragon_team = 1
        else:
            self.dragon_team = 2

        self.send_dragon_state()


    def on_dragon_left_1(self, *args):

        self.dragon_killed = get_dragon_code(self.dragon_left_1)
        self.send_dragon_state()


    def on_dragon_left_2(self, *args):

        self.dragon_killed = get_dragon_code(self.dragon_left_2)
        self.send_dragon_state()


    def on_dragon_left_3(self, *args):

        self.dragon_killed = get_dragon_code(self.dragon_left_3)
        self.send_dragon_state()


    def on_dragon_left_4(self, *args):

        self.dragon_killed = get_dragon_code(self.dragon_left_4)
        self.dragon_soul_team = 1
        self.dragon_soul = self.dragon_killed

        self.send_dragon_state()
        self.send_dragon_soul_state()


    def on_dragon_right_1(self, *args):

        self.dragon_killed = get_dragon_code(self.dragon_right_1)    
        self.send_dragon_state()


    def on_dragon_right_2(self, *args):

        self.dragon_killed = get_dragon_code(self.dragon_right_2)
        self.send_dragon_state()


    def on_dragon_right_3(self, *args):

        self.dragon_killed = get_dragon_code(self.dragon_right_3)
        self.send_dragon_state()


    def on_dragon_right_4(self, *args):

        self.dragon_killed = get_dragon_code(self.dragon_right_4)

        self.dragon_soul_team = 2
        self.dragon_soul = self.dragon_killed

        self.send_dragon_state()
        self.send_dragon_soul_state()


    def send_dragon_state(self, *args):

        if self.last_dragon_killer == 0:
            self.dragon_team = 0
        elif self.last_dragon_killer < 6:
            self.dragon_team = 1
        else:
            self.dragon_team = 2
        
        output = {
            f"/DragonState/Team": self.dragon_team,
            f"/DragonState/Type": self.dragon_killed,
            f"/DragonState/SequenceIndex": self.sequence_index,
            f"/DragonState/Killer": self.last_dragon_killer
        }

        self.send_data(**output)


    def send_dragon_soul_state(self, *args):

        output = {
            f"/DragonSoulState/Team": self.dragon_soul_team,
            f"/DragonSoulState/Type": self.dragon_soul,
            f"/DragonSoulState/SequenceIndex": self.sequence_index
        }

        self.send_data(**output)
