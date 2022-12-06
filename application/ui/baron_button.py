from kivy.app import App
import kivy.properties as kp

from ui.activator_button import ActivatorButton

class BaronButton(ActivatorButton):

    baron_stolen = kp.BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()

        self.bind(on_press=self.activate)

        self.active = self.app.special_baron_announce_event.active
        self.app.special_baron_announce_event.bind(active=self.setter('active'))

        self.disabled = self.app.special_baron_announce_event.disabled
        self.app.special_baron_announce_event.bind(disabled=self.setter('disabled'))

        self.baron_stolen = self.app.special_baron_announce_event.baron_stolen
        self.app.special_baron_announce_event.bind(baron_stolen=self.setter('baron_stolen'))

        self.on_baron_stolen()


    def on_baron_stolen(self, *args):

        if self.baron_stolen:
            self.text = "Baron\nStolen"

        else:
            self.text = "Baron\nPower Play"


    def activate(self, *args):
        self.app.special_baron_announce_event.activate(self.state)