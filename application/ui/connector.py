from kivy.app import App
from kivy.logger import Logger
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
import kivy.properties as kp

from ui.constants.colors import STATUS_COLORS, STATUS_OPTIONS


class DataButtonLayout(GridLayout):

    event_dispatcher = kp.ObjectProperty()
    connected = kp.BooleanProperty(False)
    status = kp.OptionProperty(STATUS_OPTIONS[0], options=STATUS_OPTIONS)
    status_color = kp.ListProperty(STATUS_COLORS[STATUS_OPTIONS[0]])

    enabled = kp.BooleanProperty()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()

        self.rows = 1
        self.padding = 0, 0, 10, 0

        self.activator_btn = ToggleButton(text="Connect")
        self.activator_btn.bind(on_press=self.on_event)

        self.on_enabled()


    def on_event_dispatcher(self, *args):

        self.event_dispatcher.bind(status = self.setter('status'))
        self.activator_btn.text = self.event_dispatcher.dispatch_type

        self.enabled = self.event_dispatcher.enabled
        self.event_dispatcher.bind(enabled=self.setter('enabled'))


    def on_enabled(self, *args):

        self.clear_widgets()

        if self.enabled:
            self.add_widget(self.activator_btn)


    def on_event(self, obj):

        if obj.state == "down":
            self.event_dispatcher.connected = True

        else:
            self.event_dispatcher.connected = False


    def on_status(self, *args):    
        self.status_color = STATUS_COLORS[self.status]
