import kivy.properties as kp

from data.events.data_event_dispatch import DataEventDispatcher
from data.vizrt.viz_helper import DRAGON_CODES


class DragonSoulVizSender(DataEventDispatcher):

    active = kp.BooleanProperty(False)
    dragon_soul = kp.StringProperty("default")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.vizrt.setter('input_data'))

        self.app.dragon_soul.bind(active=self.setter('active'))
        self.app.top_bar.bind(dragon_soul=self.setter('dragon_soul'))


    def on_active(self, *args):

        output = {
            "dragonSoul/anim": int(self.active),
            "dragonSoul/type": DRAGON_CODES[self.dragon_soul]
        }

        self.send_data(**output)

    def on_game_reset(self, *args):

        output = {
            "dragonSoul/anim": 0,
            "dragonSoul/type": 0
        }

        self.app.vizrt.send_now(output)
