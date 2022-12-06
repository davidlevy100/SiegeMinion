from functools import partial

from kivy.app import App
import kivy.properties as kp

from ui.activator_button import ActivatorButton

class DragonSoulButton(ActivatorButton):
    
    dragon_soul = kp.StringProperty("default")
    dragon_soul_active = kp.BooleanProperty(False)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()

        self.active = self.app.dragon_soul.active
        self.app.dragon_soul.bind(active=self.setter('active'))

        self.dragon_soul_active = self.app.dragon_soul.dragon_soul_active
        self.app.dragon_soul.bind(dragon_soul_active=self.setter('dragon_soul_active'))

        self.app.dragon_soul.bind(dragon_soul=self.setter('dragon_soul'))

        self.bind(on_press=self.activate)

        self.on_dragon_soul()
        self.on_dragon_soul_active()



    def on_dragon_soul_active(self, *args):

        self.disabled = not self.dragon_soul_active


    def on_dragon_soul(self, *args):

        if self.dragon_soul == "default":
            self.text = "Dragon\r\nSoul"
        else:
            self.text = f"{self.dragon_soul.title()}\r\nSoul"


    def activate(self, *args):
        self.app.dragon_soul.activate(self.state)
