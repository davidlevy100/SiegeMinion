import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher


DRAGON_CODES = {
    "": 0,
    None: 0,
    "default": 0,
    "air": 1,
    "cloud": 1,
    "fire": 2,
    "infernal": 2,
    "earth": 3,
    "mountain": 3,
    "water": 4,
    "ocean": 4,
    "elder": 5
}

class NextDragonOSCSender(DataEventDispatcher):

    next_dragon_name = kp.StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.osc.setter('input_data'))

        self.app.next_dragon.bind(
            next_dragon_name=self.setter('next_dragon_name')
        )
        self.app.next_dragon.bind(
            next_dragon_name=self.setter('next_dragon_name')
        )
    
    
    def on_next_dragon_name(self, *args):

        output = {
            "/NextDragon/Type": DRAGON_CODES.get(self.next_dragon_name, 0),
            "/NextDragon/SequenceIndex": self.app.next_dragon.sequence_index
        }

        self.send_data(**output)
