from kivy.uix.togglebutton import ToggleButton
import kivy.properties as kp


class ActivatorButton(ToggleButton):

    active = kp.BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.state = "normal"


    def on_active(self, *args):

        if self.active:
            self.state = "down"
        else:
            self.state = "normal"