from datetime import datetime

import kivy.properties as kp

from data.events.data_event_dispatch import DataEventDispatcher
from data.vizrt.viz_helper import DRAGON_CODES

STATES = {
    "alive": 1,
    "buff_active": 2,
    "buff_ended": 3,
    "respawning": 0
}


class NextDragonVizSender(DataEventDispatcher):

    next_dragon_name = kp.StringProperty("")
    respawn_timer_string = kp.StringProperty("---")
    state = kp.OptionProperty(
        "respawning", 
        options=[
            "alive",
            "buff_active",
            "buff_ended",
            "respawning"
        ]
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.vizrt.setter('input_data'))

        self.app.next_dragon.bind(next_dragon_name=self.setter('next_dragon_name'))
        self.app.next_dragon.bind(respawn_timer_string=self.setter('respawn_timer_string'))
        self.app.next_dragon.bind(state=self.setter('state'))


    def on_game_reset(self, *args):

        output = {
            "dragon/anim": 0,
            "dragon/cd": "---",
            "dragon/type": 0
        }

        self.app.vizrt.send_now(output)


    def on_next_dragon_name(self, *args):

        output = {
            "dragon/type": DRAGON_CODES[self.next_dragon_name]
        }

        self.send_data(**output)


    def on_respawn_timer_string(self, *args):

        output = {
            "dragon/cd": self.respawn_timer_string,
            "dragon/anim": STATES[self.state]
        }

        self.send_data(**output)


    def on_state(self, *args):

        output = {
            "dragon/anim": STATES[self.state]
        }

        self.send_data(**output)
