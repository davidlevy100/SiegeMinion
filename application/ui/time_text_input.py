import re

from kivy.app import App
from kivy.uix.textinput import TextInput
import kivy.properties as kp
from kivy.logger import Logger

from data.esports.stats import convert_MS_string_to_milliseconds
from data.esports.stats import convert_milliseconds_to_HMS_string

VALIDTIME = [1,1,1,1]
WARNINGTIME = [1,1,0,1]
INVALIDTIME = [1,0,0,1]

ALLOWEDCHARS = "01234567890:"

class TimeTextInput(TextInput):

    pat = re.compile('([0-9]|[0-9][0-9]):[0-5][0-9]')
    is_valid_time = kp.BooleanProperty(False)
    milliseconds = kp.NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()

        self.hint_text = "00:00"
        self.multiline = False
        self.write_tab = False
        self.background_color = VALIDTIME


    def on_is_valid_time(self, *args):

        if self.is_valid_time:
            self.background_color = VALIDTIME
        else:
            self.background_color = WARNINGTIME


    def on_text(self, *args):

        match = self.pat.search(self.text)

        if match is None:
            self.is_valid_time = False
        else:
            self.is_valid_time = True
            self.text = match.group()
            self.milliseconds = convert_MS_string_to_milliseconds(self.text)


    def on_milliseconds(self, *args):

        self.text = convert_milliseconds_to_HMS_string(self.milliseconds)


    def insert_text(self, substring, from_undo=False):

        if ":" in self.text:
            newString = "".join([x for x in substring if x.isdigit()])

        else:
            newString = "".join([x for x in substring if x in ALLOWEDCHARS])

        return super().insert_text(newString, from_undo=from_undo)


    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        super().keyboard_on_key_down(window, keycode, text, modifiers)

        if keycode[1] == 'up':
            self.milliseconds = self.milliseconds + 1000

        elif keycode[1] == 'down':
            self.milliseconds = self.milliseconds - 1000
    

    def initialize(self, *args):

        self.is_valid_time = False
        self.text = ""
        self.background_color = WARNINGTIME
