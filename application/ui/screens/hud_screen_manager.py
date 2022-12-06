from kivy.logger import Logger
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
import kivy.properties as kp


class HUDScreenManager(ScreenManager):

    game_reset = kp.StringProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.transition = NoTransition()

    
    def on_game_reset(self, *args):
        raise NotImplementedError
