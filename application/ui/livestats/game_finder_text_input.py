from kivy.app import App
import kivy.properties as kp
from kivy.uix.textinput import TextInput


from ui.constants.text import GAMEFINDER_HINT_TEXT

class GameFinderTextInput(TextInput):

    platform_game_id = kp.StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()

        self.app.bind(platform_game_id=self.setter('text'))
        self.bind(text=self.app.setter('platform_game_id'))
        
        self.hint_text = GAMEFINDER_HINT_TEXT
        self.readonly = False
        self.multiline = False
        self.padding = [6, 1, 6, 0]
        self.write_tab = False
        self.size_hint_x = 2.25
