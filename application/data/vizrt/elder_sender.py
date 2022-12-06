from datetime import datetime

import kivy.properties as kp

from data.events.data_event_dispatch import DataEventDispatcher

STATES = {
    "alive": 1,
    "buff_active": 2,
    "spawning": 0,
    "respawning": 0
}


class ElderVizSender(DataEventDispatcher):

    # active = kp.BooleanProperty(True)
    tricode_left = kp.StringProperty()
    tricode_right = kp.StringProperty()

    # Output Properties
    buff_timer_string = kp.StringProperty("00:00")
    team = kp.StringProperty(" ")
    teamID = kp.NumericProperty(0)

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
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.game_data.bind(tricode_left=self.setter('tricode_left'))
        self.app.game_data.bind(tricode_right=self.setter('tricode_right'))

        # self.app.elder_dragon.bind(active=self.setter('active'))
        self.app.elder_dragon.bind(buff_timer_string=self.setter('buff_timer_string'))
        self.app.elder_dragon.bind(team=self.setter('team'))
        self.app.elder_dragon.bind(teamID=self.setter('teamID'))

        self.app.elder_dragon.bind(respawn_timer_string=self.setter('respawn_timer_string'))
        self.app.elder_dragon.bind(state=self.setter('state'))

        self.bind(output=self.app.vizrt.setter('input_data'))


    def on_game_reset(self, *args):

        output = {
            "elder/anim": STATES[self.state],
            "elder/buffTimer": self.buff_timer_string,
            "elder/cd":  self.respawn_timer_string,
            "elder/tri": self.team,
            "elder/team": self.teamID
        }

        self.app.vizrt.send_now(output)


    def on_state(self, *args):

        output = {
            "elder/anim": STATES[self.state],
        }

        self.send_data(**output)


    def on_team(self, *args):

        output = {
            "elder/tri": self.team
        }

        self.send_data(**output)


        


    def on_buff_timer_string(self, *args):

        output = {
            "elder/buffTimer": self.buff_timer_string
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
            "elder/team": self.teamID / 100
        }

        self.send_data(**output)


    def on_respawn_timer_string(self, *args):

        output = {
            "elder/cd": self.respawn_timer_string
        }

        self.send_data(**output)
