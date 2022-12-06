
from kivy.uix.textinput import TextInput
import kivy.properties as kp

class IntegerInput(TextInput):

    value = kp.NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.multiline = False
        self.write_tab = False
        self.padding = 4, 0

        self.on_value()


    def on_value(self, *args):
        self.text = f"{self.value}"


    def on_size(self, *args):
        self.font_size = self.size[1] * 0.8


    def insert_text(self, substring, from_undo=False):

        if substring.isnumeric():
            self.value = int(substring)


    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        super().keyboard_on_key_down(window, keycode, text, modifiers)

        if keycode[1] == 'up':
            self.value = self.value + 1

        elif keycode[1] == 'down':
            self.value = self.value - 1
