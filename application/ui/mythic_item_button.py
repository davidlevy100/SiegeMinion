from functools import partial

from kivy.app import App
import kivy.properties as kp

from ui.activator_button import ActivatorButton

class MythicItemButton(ActivatorButton):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()

        self.active = self.app.mythic_item.active
        self.app.mythic_item.bind(active=self.setter('active'))

        self.bind(on_press=self.activate)

        self.text = "Mythic\nItem"

        self.disabled = self.app.mythic_item.disabled
        self.app.mythic_item.bind(disabled=self.setter('disabled'))




    def activate(self, *args):
        self.app.mythic_item.activate(self.state)