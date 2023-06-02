import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher
from data.vizrt.viz_helper import get_dragon_code

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
            "/NextDragon/Type": get_dragon_code(self.next_dragon_name),
            "/NextDragon/SequenceIndex": self.app.next_dragon.sequence_index
        }

        self.send_data(**output)
