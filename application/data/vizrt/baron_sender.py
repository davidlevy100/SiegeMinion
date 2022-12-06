from datetime import datetime

import kivy.properties as kp

from data.events.data_event_dispatch import DataEventDispatcher

STATES = {
    "alive": 1,
    "buff_active": 2,
    "spawning": 0,
    "respawning": 0
}


class BaronVizSender(DataEventDispatcher):

    # active = kp.BooleanProperty(True)
    tricode_left = kp.StringProperty()
    tricode_right = kp.StringProperty()

    # Output Properties
    buff_timer_string = kp.StringProperty("00:00")

    gold_string = kp.StringProperty("")

    respawn_timer_string = kp.StringProperty("---")

    state = kp.OptionProperty(
        "spawning", 
        options=[
            "alive",
            "buff_active",
            "spawning",
            "respawning"
        ]
    )

    team = kp.StringProperty(" ")
    teamID = kp.NumericProperty(0)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.game_data.bind(tricode_left=self.setter('tricode_left'))
        self.app.game_data.bind(tricode_right=self.setter('tricode_right'))

        #self.app.baron_power_play.bind(active=self.setter('active'))
        self.app.baron_power_play.bind(buff_timer_string=self.setter('buff_timer_string'))
        self.app.baron_power_play.bind(gold_string=self.setter('gold_string'))
        self.app.baron_power_play.bind(respawn_timer_string=self.setter('respawn_timer_string'))
        self.app.baron_power_play.bind(state=self.setter('state'))
        self.app.baron_power_play.bind(team=self.setter('team'))
        self.app.baron_power_play.bind(teamID=self.setter('teamID'))
        

        self.bind(output=self.app.vizrt.setter('input_data'))


    def on_game_reset(self, *args):

        output = {
            "baron/anim": STATES[self.state],
            "baron/buffTimer": self.buff_timer_string,
            "baron/cd":  self.respawn_timer_string,
            "baron/gold": f'\"\"{self.gold_string}\"\"',
            "baron/team": self.teamID,
            "baron/tri": self.team
        }

        self.app.vizrt.send_now(output)


    def on_state(self, *args):

        output = {
            "baron/anim": STATES[self.state],
        }

        self.send_data(**output)


    def on_team(self, *args):

        output = {
            "baron/tri": self.team
        }

        self.send_data(**output)


    def on_buff_timer_string(self, *args):

        output = {
            "baron/buffTimer": self.buff_timer_string
        }

        self.send_data(**output)


    def on_gold_string(self, *args):

        str_gold = self.gold_string

        if str_gold == "+0":
            str_gold = ""

        output = {
            "baron/gold": f'\"\"{str_gold}\"\"'
        }

        self.send_data(**output)


    def on_teamID(self, *args):
        
        if self.teamID == 100:
            self.team = self.tricode_left

        elif self.teamID == 200:
            self.team = self.tricode_right

        else:
            self.team = ""

        output = {
            "baron/team": self.teamID / 100
        }

        self.send_data(**output)


    def on_respawn_timer_string(self, *args):

        output = {
            "baron/cd": self.respawn_timer_string
        }

        self.send_data(**output)
