from kivy.uix.label import Label
import kivy.properties as kp

from data.esports.stats import convert_milliseconds_to_HMS_string

class ClockLabel(Label):

    input_time = kp.NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = convert_milliseconds_to_HMS_string(milliseconds=self.input_time)

    def on_input_time(self, *args):
        self.text = convert_milliseconds_to_HMS_string(milliseconds=self.input_time)
