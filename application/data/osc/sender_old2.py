from kivy.logger import Logger
import kivy.properties as kp

from data.osc.udp import SimpleMulticastClient
from data.events.engine_dispatch import EngineDispatcher
from ui.constants.text import OSC_BUTTON_TEXT


class MulticastSender(EngineDispatcher):

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

    client = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dispatch_type = OSC_BUTTON_TEXT


    def open_connection(self, *args):

        self.close_connection()
        self.client = SimpleMulticastClient(self.ip, self.port)

        self.status = "good"


    def close_connection(self, *args):

        if self.client is not None:
            self.client.close()
            self.client = None

            self.status = "off"


    def on_input_data(self, *args):

        if (not self.enabled or
            not self.connected
        ):
            return

        for key, value in self.input_data.items():
            self.client.send_message(key, value)

    
    def send_now(self, messages):

        if (not self.enabled or
            not self.connected
        ):
            return

        for key, value in messages.items():
            self.client.send_message(key, value)


    def get_config(self, *args):
        pass

    def update_engine(self, message, *args):
        pass

    def reset_engine(self, *args):
        pass
