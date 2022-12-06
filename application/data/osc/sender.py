from functools import partial

from kivy.clock import Clock
from kivy.app import App
from kivy.event import EventDispatcher
import kivy.properties as kp
from kivy.logger import Logger

from data.osc.udp import ImprovedUDPClient
from data.osc.udp import SimpleMulticastClient

from ui.constants.colors import STATUS_OPTIONS

class OSCSender(EventDispatcher):

    transmission_type = kp.StringProperty("Unicast")

    enabled = kp.BooleanProperty(True)

    input_data = kp.DictProperty()

    app = None
    clients = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        self.check_settings()


    def check_settings(self, *args):

        self.enabled = int(self.app.config.get("OSC", "enabled"))
        self.transmission_type = self.app.config.get("OSC", "transmission_type")

        if self.transmission_type == "Unicast":
            self.create_unicast_clients()

        elif self.transmission_type == "Multicast":
            self.create_multicast_clients()


    def clear_clients(self, *args):

        if len(self.clients) == 0:
            return

        for this_client in self.clients:

            try:
                this_client.close()

            except Exception as e:
                Logger.exception(f"Error: {e}")

        self.clients.clear()


    def create_unicast_clients(self, *args):

        self.clear_clients()

        for i in range(1, 25):

            this_enabled = bool(int(self.app.config.get('OSC', f"enabled{i}")))

            if this_enabled:

                this_ip = self.app.config.get('OSC', f"ip{i}")
                this_port = int(self.app.config.get('OSC', f"port{i}"))

                Clock.schedule_once(partial(self.create_unicast_client, this_ip, this_port))

        
    def create_unicast_client(self, ip, port, *args):

        try:
            this_client = ImprovedUDPClient(ip, port)
            self.clients.append(this_client)

            LogMessage = (
                f"OSC Event: Creating Unicast OSC Client sending to {ip}:{port}"
            )
            Logger.info(LogMessage)

        except Exception as e:
            Logger.exception(f"Error: {e}")



    def create_multicast_clients(self, ip, port, *args):

        self.clear_clients()

        for i in range(1, 25):

            this_enabled = bool(int(self.app.config.get('OSC', f"enabled{i}")))

            if this_enabled:

                this_ip = self.app.config.get('OSC', f"ip{i}")
                this_port = int(self.app.config.get('OSC', f"port{i}"))

                Clock.schedule_once(partial(self.create_multicast_client, this_ip, this_port))


    def create_multicast_client(self, ip, port, *args):

        try:
            this_client = SimpleMulticastClient(ip, port)
            self.clients.append(this_client)

            LogMessage = (
                f"OSC Event: Creating Multicast OSC Client sending to {ip}:{port}"
            )
            Logger.info(LogMessage)

        except Exception as e:
            Logger.exception(f"Error: {e}")


    def on_input_data(self, *args):

        if len(self.clients) == 0:
            return

        if self.enabled:
            for key, value in self.input_data.items():
                for this_client in self.clients:
                    this_client.send_message(key, value)
    

    def send_now(self, messages):

        if len(self.clients) == 0:
            return

        if self.enabled:
            for key, value in messages.items():
                for this_client in self.clients:
                    this_client.send_message(key, value)
