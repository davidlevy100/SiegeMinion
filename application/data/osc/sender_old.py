import random

from pythonosc.udp_client import SimpleUDPClient

from kivy.app import App
from kivy.event import EventDispatcher
import kivy.properties as kp
from kivy.logger import Logger

from ui.constants.colors import STATUS_OPTIONS

class OSCSender(EventDispatcher):

    ip = kp.ConfigParserProperty(
        "127.0.0.1",
        "OSC",
        "ip",
        "app"
    )

    port = kp.ConfigParserProperty(
        64228,
        "OSC",
        "port",
        "app",
        val_type=int
    )

    enabled = kp.ConfigParserProperty(
        0,
        "OSC",
        "enabled",
        "app",
        val_type=int
    )

    input_data = kp.DictProperty()
    dispatch_type = kp.StringProperty("")

    status = kp.OptionProperty(
        STATUS_OPTIONS[0],
        options=STATUS_OPTIONS
    )

    app = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        self.client = SimpleUDPClient(self.ip, self.port)


    def on_input_data(self, *args):

        if self.enabled:
            for key, value in self.input_data.items():
                self.client.send_message(key, value)
    

    def send_now(self, messages):

        if self.enabled:
            for key, value in messages.items():
                self.client.send_message(key, value) 
    