from kivy.uix.label import Label
import kivy.properties as kp
from kivy.graphics import Color, Rectangle


class NumericLabel(Label):

    input_data = kp.NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = f"{self.input_data}"

    def on_input_data(self, *args):
        self.text = f"{self.input_data}"


class FormattedNumericLabel(Label):

    input_data = kp.NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = f"{self.input_data:,d}"

    def on_input_data(self, *args):
        self.text = f"{self.input_data:,d}"


class BlackNumericLabel(NumericLabel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(
                pos=self.pos, 
                size=self.size
            )
