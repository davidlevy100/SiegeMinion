import re
import subprocess
from urllib.parse import urlencode
from base64 import urlsafe_b64encode
from datetime import datetime
from pathlib import Path
import json

from kivy.app import App
import kivy.properties as kp
from kivy.logger import Logger
from kivy.storage.jsonstore import JsonStore

from data.events.polling_dispatch import PollingDispatcher

from ui.constants.text import LCU_CLIENT_TEXT

LCU_POLLING_INTERVAL = 0.5
TEST_CHAMP_SELECT_DATA = Path().joinpath('data', 'test_data', 'lcu_champ_select.json')


class LeagueNotRunningException(Exception):
    """ Exception Raised if the 
        League Client is not running """


class LCUPollingDispatcher(PollingDispatcher):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dispatch_type = LCU_CLIENT_TEXT
        self.server_url = "127.0.0.1"
        self.update_interval = 0.5


    def get_process(self):
        """ Checks if the League Client is running
        The function determines whether the client is running and returns a string
        containing the commandline arguments that were passed when the client was
        being launched.
        Returns:
            A string (the string is empty if the client isn't running)
        """

        # Using the WMIC command to retrieve running processes.
        cmd = 'WMIC PROCESS get Caption,Commandline'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

        result = ''

        for line in proc.stdout:
            line = line.decode('utf-8')

            if 'LeagueClientUx.exe' in line:
                # Formatting the string for easier processing
                result = re.sub(' +', ' ', line).rstrip()
                break

        return result


    def get_connection_details(self):
        """ Retrieves the info required to connect to the LCU Api
        The function returns the port and the authentication token that the League
        client that is currently running is using for its api
        Returns:
            A tuple containing the token(string) and the port(string)
        """

        command_line = self.get_process()

        if command_line == '':
            raise LeagueNotRunningException

        token = re.search(r'\"--remoting-auth-token=(\S+)\"',
                        command_line).group(1)
        port = re.search(r'\"--app-port=(\S+)\"', command_line).group(1)

        return (token, port)


    def construct_request(self, *args):

        try:
            self.token, self.server_port = self.get_connection_details()

        except LeagueNotRunningException:
            Logger.exception(f"Data Polling Error: {datetime.now().strftime('%r')} League Client not Running")


        hash_string = urlsafe_b64encode(
            f"riot:{self.token}".encode('utf-8')
        ).decode('utf-8')

        self.headers = {
            "Authorization": f"Basic {hash_string}",
            'Accept': "application/json",
            'Cache-Control': "no-cache",
            'Host': f"{self.server_url}:{self.server_port}",
            'accept-encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

        self.full_url = f"https://{self.server_url}:{self.server_port}/lol-champ-select/v1/session"


class DevLCUPollingDispatcher(LCUPollingDispatcher):

    def get_connection_details(self):

        return ("developer", 9090)


class TestLCUPollingDispatcher(LCUPollingDispatcher):

    key = kp.NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dispatch_type = f"Test {self.dispatch_type}"

        with open(TEST_CHAMP_SELECT_DATA, "r") as f:
            self.test_champ_data = json.load(f)

        self.update_interval = 1.0


    def construct_request(self, *args):
        pass


    def get_data(self, *args):

        result = self.test_champ_data[f"{self.key}"]["message"]
        self.handle_request(request=None, result=result)
        self.key += 1

        if self.key >= len(self.test_champ_data):
            self.key = len(self.test_champ_data) - 1


    def initialize(self, *args):
        super().initialize()
        self.key = 0


class RecordingLCUPollingDispatcher(LCUPollingDispatcher):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_store()
        

    def set_store(self, *args):

        self.index = 0

        store_path = Path().joinpath(
            "logs", 
            f"champ_select_{datetime.now().strftime('%b_%d_%H_%M_%S')}.json"
        )

        self.store = JsonStore(store_path)


    def initialize(self, *args):
        super().initialize()
        self.set_store()


    def handle_request(self, request, result):

        if self.connected:
            self.output = result
            self.store.put(f"{self.index}", message=result)
            self.index += 1
