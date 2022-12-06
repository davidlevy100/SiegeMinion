from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from ui.activator_button import ActivatorButton
import kivy.properties as kp


class SponsorLayout(GridLayout):

    section = kp.StringProperty()
    prefix = kp.StringProperty()
    sponsor_name = kp.StringProperty("")
    target = kp.ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rows = 1

        self.app = App.get_running_app()

        self.my_button = ActivatorButton(
            text=self.sponsor_name,
            on_press=self.activate,
            halign="center"
        )
        self.bind(sponsor_name=self.my_button.setter('text'))

    
    def on_sponsor_name(self, *args):

        self.clear_widgets()

        if self.sponsor_name != "":
            self.add_widget(self.my_button)


    def on_target(self, *args):

        if self.target is not None:
            self.target.bind(active=self.my_button.setter('active'))


    def on_active(self, *args):

        if self.active:
            self.state = "down"
        
        else:
            self.state = "normal"


    def on_prefix(self, *args):
        self.sponsor_name = self.app.config.get(self.section, f"{self.prefix}_name").replace(" ", "\n")
        self.app.config.add_callback(self.set_sponsor_name, self.section, f"{self.prefix}_name")


    def set_sponsor_name(self, *args):

        self.sponsor_name = args[-1].replace(" ", "\n")

        self.clear_widgets()

        if self.sponsor_name != "":
            self.add_widget(self.my_button)

    
    def activate(self, *args):
        if self.target is not None:
            self.target.activate(self.my_button.state)
