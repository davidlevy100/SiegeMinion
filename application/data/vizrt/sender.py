from datetime import datetime
from functools import partial
import select
import socket

from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.logger import Logger
import kivy.properties as kp

from data.events.engine_dispatch import EngineDispatcher
from ui.constants.text import VIZ_BUTTON_TEXT
from ui.constants.colors import STATUS_OPTIONS


class VizrtDispatcher(EngineDispatcher):

    enabled = kp.ConfigParserProperty(
        0,
        "vizrt",
        "enabled",
        "app",
        val_type=int
    )

    sockets = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dispatch_type = VIZ_BUTTON_TEXT


    def on_enabled(self, *args):

        if not self.enabled:
            self.close_connection()


    def get_config(self, *args):
        pass
        

    def open_connection(self, *args):

        self.sockets.clear()

        for i in range(1, 9):
            this_enabled = bool(int(self.app.config.get('vizrt', f"enabled{i}")))

            if this_enabled:
                this_ip = self.app.config.get('vizrt', f"ip{i}")
                this_port = int(self.app.config.get('vizrt', f"tcp_port{i}"))

                Clock.schedule_once(partial(self.create_socket, this_ip, this_port))
               

    def create_socket(self, ip, port, *args):

        try:
            this_socket = socket.socket()
            this_socket.connect((ip, port))
            this_socket.setblocking(0)

            reset_bytes = self.create_reset_message()
            this_socket.sendall(reset_bytes)

            self.sockets.append(this_socket)
            self.status = "good"

        except Exception as e:
            Logger.exception(f"Error: {e}")
            self.status = "warning"


    def create_reset_message(self, *args):
        raise NotImplementedError


    def close_connection(self, *args):

        for this_socket in self.sockets:
            try:
                this_socket.shutdown(socket.SHUT_RDWR)
                this_socket.close()

            except Exception as e:
                Logger.exception(f"Error: {e}")

        self.sockets.clear()
        self.status = "off"


    def update_engine(self, message, *args):

        if (not self.enabled or
            not self.connected or 
            len(self.sockets) == 0
        ):
            return

        if len(message) > 0:

            b = message.encode("utf-8")

            try:

                readable, writable, errors = select.select(
                    self.sockets, 
                    self.sockets, 
                    self.sockets,
                    0
                )

                for r in readable:

                    return_message = r.recv(1024).decode('utf-8')

                    if "ERROR" in return_message:
                        Logger.info(f"VizRT Error Response: {return_message}")
                
                for w in writable:
                    self.status = "good"
                    w.send(b)

                for e in errors:
                    self.status = "warning"

            except Exception as e:
                self.status = "warning"
                Logger.exception(f"Error: {e}")


class SharedMemorySender(VizrtDispatcher):

    def construct_message(self, *args, **kwargs):

        viz_message = ""

        for key, value in kwargs.items():

            viz_message += f"{key}|{value}\0"

        return viz_message


class DatapoolSender(VizrtDispatcher):

    # config properties
    layer = kp.ConfigParserProperty(
        "",
        "vizrt",
        "layer",
        "app"
    )

    # Construct message for Datapool
    def construct_message(self, *args, **kwargs):

        viz_message = f"-1 {self.layer}*FUNCTION*DataPool*Data SET "

        for key, value in kwargs.items():
            viz_message += f"{key}={value};"

        viz_message += " \0"

        return viz_message


    def create_reset_message(self, *args):

        reset_message = {
            "RESET": str(datetime.now())
        }

        message = self.construct_message(**reset_message)
        message_bytes = message.encode("utf-8")

        return message_bytes
