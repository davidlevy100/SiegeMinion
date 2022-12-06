from datetime import datetime

from kivy.app import App

from kivy.event import EventDispatcher
import kivy.properties as kp
from kivy.logger import Logger

class DataEventDispatcher(EventDispatcher):

    game_reset = kp.StringProperty("")
    output = kp.DictProperty()
    update_now = kp.StringProperty()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()
        self.app.bind(game_reset=self.setter('game_reset'))


    def on_game_reset(self, *args):
        pass

    
    def on_update_now(self, *args):
        pass


    def update(self, *args):
        pass

    
    def send_now(self, message, *args):
        pass


    def send_data(self, *args, **kwargs):

        """Expects a key/value pairs in the form of:
        key=value

        example1: 
        data = {key: value}
        self.send_data(**data)

        example2: 
        self.send_data(key=value)

        """
        
        self.output.update(kwargs)
