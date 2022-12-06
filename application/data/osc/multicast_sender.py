from collections import Iterable
import socket
from typing import Union

from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.osc_message import OscMessage
from pythonosc.osc_bundle import OscBundle

from kivy.app import App
from kivy.event import EventDispatcher
import kivy.properties as kp
from kivy.logger import Logger

from ui.constants.colors import STATUS_OPTIONS


class MulticastUDPClient(object):
    """OSC client to send :class:`OscMessage` or :class:`OscBundle` via UDP"""

    def __init__(self, address: str, port: int) -> None:
        """Initialize client

        As this is UDP it will not actually make any attempt to connect to the
        given server at ip:port until the send() method is called.

        Args:
            address: IP address of server
            port: Port of server
        """
        for addr in socket.getaddrinfo(address, port, type=socket.SOCK_DGRAM):
            af, socktype, protocol, canonname, sa = addr

            try:
                self._sock = socket.socket(af, socktype)
            except OSError:
                continue
            break

        self._sock.setblocking(0)
        self._sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
        
        self._address = address
        self._port = port

    def send(self, content: Union[OscMessage, OscBundle]) -> None:
        """Sends an :class:`OscMessage` or :class:`OscBundle` via UDP

        Args:
            content: Message or bundle to be sent
        """
        self._sock.sendto(content.dgram, (self._address, self._port))


    def close(self):
        self._sock.close()


class SimpleMulticastClient(MulticastUDPClient):
    """Simple OSC client that automatically builds :class:`OscMessage` from arguments"""

    def send_message(self, address: str, value: Union[int, float, bytes, str, bool, tuple, list]) -> None:
        """Build :class:`OscMessage` from arguments and send to server

        Args:
            address: OSC address the message shall go to
            value: One or more arguments to be added to the message
        """
        builder = OscMessageBuilder(address=address)
        if value is None:
            values = []
        elif not isinstance(value, Iterable) or isinstance(value, (str, bytes)):
            values = [value]
        else:
            values = value
        for val in values:
            builder.add_arg(val)
        msg = builder.build()
        self.send(msg)


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

        self.client = SimpleMulticastClient(self.ip, self.port)


    def on_input_data(self, *args):

        if self.enabled:
            for key, value in self.input_data.items():
                self.client.send_message(key, value)
    

    def send_now(self, messages):

        if self.enabled:
            for key, value in messages.items():
                self.client.send_message(key, value) 
    