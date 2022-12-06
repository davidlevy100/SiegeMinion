from collections.abc import Iterable
import socket
from typing import Union

from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.osc_message import OscMessage
from pythonosc.osc_bundle import OscBundle

from pythonosc.udp_client import SimpleUDPClient

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


    def close(self, *args):
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


class ImprovedUDPClient(SimpleUDPClient):

    """adds a close() method to simple UDP Client"""

    def close(self, *args):
        self._sock.close()
