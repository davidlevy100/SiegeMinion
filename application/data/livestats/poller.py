import json
from pathlib import Path
from socket import gethostbyname
from urllib.parse import urlencode
from urllib.parse import urlparse

from kivy.app import App
import kivy.properties as kp

from data.events.polling_dispatch import PollingDispatcher

from ui.constants.text import LIVESTATS_BUTTON_TEXT


TEST_LIVESTATS_DATA = Path().joinpath('data', 'test_data', 'livestats')


class LiveStatsPollingDispatcher(PollingDispatcher):

    api_key = kp.StringProperty("")
    platform_game_id = kp.StringProperty("")
    pagination_token = kp.StringProperty("")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.bind(platform_game_id=self.setter('platform_game_id'))
        self.app.bind(game_reset=self.setter('game_reset'))
        self.bind(connected=self.app.setter('connected'))
        self.dispatch_type = LIVESTATS_BUTTON_TEXT


    def initialize(self, *args):

        super().initialize()
        self.pagination_token = ""
        


    def construct_request(self, *args):

        base_url = self.app.config.get(
            'Livestats',
            'base_url'
        )

        if base_url[-1] == "/":
            base_url = base_url[:-1]

        self.server_url = base_url
        self.server_port = ""
        self.api_key = self.app.config.get(
            'Livestats',
            'api_key'
        )
        
        self.update_interval = float(
            self.app.config.get(
                'Livestats',
                'polling_interval'
            )
        )

        self.headers = {
            'Accept': "application/json",
            'Cache-Control': "no-cache",
            'cache-control': "no-cache",
            'Connection': "keep-alive",
            'Host': "raw-stats-api.ewp.gg",
            'x-api-key': self.api_key
        }

        self.full_url = f"{self.server_url}/platformGames/{self.platform_game_id}/events"


    def handle_request(self, request, result):

        super().handle_request(request, result)

        #update self.pagination_token
        if "nextPageToken" in result:
            self.pagination_token = result["nextPageToken"]

            querystring = {
                "paginationToken": self.pagination_token
            }

            myQuery = urlencode(querystring)

            self.full_url = f"{self.server_url}/platformGames/{self.platform_game_id}/events?{myQuery}"


class PlaybackPollingDispatcher(PollingDispatcher):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dispatch_type = "TEST DATA"
        self.index = 0


    def construct_request(self, *args):

        self.update_interval = 0.1


    def get_data(self, dt):

        if self.connected:

            file_path = TEST_LIVESTATS_DATA.joinpath(f"{self.index}.json")

            if file_path.exists():

                try:

                    data = json.loads(file_path.read_text())
                    self.output = data
                    self.index = self.index + 1

                except json.decoder.JSONDecodeError as e:
                    print(self.index, e)

            else:
                self.connected = False


    def initialize(self, *args):

        super().initialize()
        self.index = 0
