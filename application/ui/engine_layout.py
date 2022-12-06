from kivy.app import App
from kivy.logger import Logger
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
import kivy.properties as kp

from ui.constants.colors import STATUS_COLORS, STATUS_OPTIONS
from ui.constants.text import ENGINE_TXT


class EngineLayout(GridLayout):

    event_dispatchers = kp.ListProperty([])
    connected = kp.BooleanProperty(False)
    enabled = kp.BooleanProperty()

    status = kp.OptionProperty(STATUS_OPTIONS[0], options=STATUS_OPTIONS)
    status_color = kp.ListProperty(STATUS_COLORS[STATUS_OPTIONS[0]])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()

        self.rows = 1
        self.padding = 0, 0, 10, 0

        self.activator_btn = ToggleButton(text=ENGINE_TXT)
        self.activator_btn.bind(on_press=self.on_event)

        self.on_enabled()


    def on_event_dispatchers(self, *args):

        enabled_count = 0

        for this_dispatcher in self.event_dispatchers:

            if this_dispatcher.enabled:

                enabled_count += 1

                self.bind(connected=this_dispatcher.setter('connected'))
                this_dispatcher.bind(status=self.setter('status'))

            this_dispatcher.bind(enabled=self.setter('enabled'))

        if enabled_count > 0:
            self.add_widget(self.activator_btn)

    
    def on_event(self, obj):

        if obj.state == "down":
            self.connected = True

        else:
            self.connected = False


    def on_enabled(self, *args):

        print(args)

        self.clear_widgets()

        for this_dispatcher in self.event_dispatchers:
            self.unbind(connected=this_dispatcher.setter('connected'))
            this_dispatcher.unbind(enabled=self.setter('enabled'))
            this_dispatcher.unbind(status=self.setter('status'))

        self.on_event_dispatchers()
