  
import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher


class DataController(DataEventDispatcher):

    active = kp.BooleanProperty(False)
    active_dispatcher = kp.ObjectProperty(allownone=True)

    def on_active_dispatcher(self, *args):

        if self.active_dispatcher is None:
            self.active = False
        else:
            self.active = True

    def set_active_dispatcher(self, dispatcher):
        self.active_dispatcher = dispatcher


    def on_game_reset(self, *args):

        self.active = False
        self.active_dispatcher = None
