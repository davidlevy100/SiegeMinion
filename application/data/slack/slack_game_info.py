from datetime import datetime, timezone
import json

import kivy.properties as kp
from kivy.logger import Logger

from data.slack.slack_dispatcher import SlackDispatcher


class GameInfoSlackDispatcher(SlackDispatcher):

    game_info_event = kp.DictProperty({})

    config_version = kp.ConfigParserProperty(
        "",
        "Data Dragon",
        "game_version",
        "app"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.live_data.bind(game_info_event=self.setter('game_info_event'))
        
        self.section = "Slack"


    def on_game_info_event(self, *args):

        if ("gameID" in self.game_info_event and
            "platformID" in self.game_info_event and
            "gameName" in self.game_info_event and
            "gameVersion" in self.game_info_event
        ):

            text = f'{self.game_info_event["gameName"]}|{self.game_info_event["platformID"]}_{self.game_info_event["gameID"]}|{self.game_info_event["gameVersion"]}'

            now = datetime.now(timezone.utc)
            unix_time = int(now.timestamp())
            now_string = now.strftime("%c %Z")

            messages = [
                f"Connected to game on <!date^{unix_time}^{{date}} at {{time}}|{now_string}>\r\n",
                f'Game Name: `{self.game_info_event["gameName"]}`\r\n',
                f'Platform_GameID: `{self.game_info_event["platformID"]}_{self.game_info_event["gameID"]}`\r\n',
                f'Game Version: {self.game_info_event["gameVersion"]}\r\n',
                f'DDragon Version: {self.config_version}\r\n'
                ":fistbump:"
            ]

            blocks = self.basic_block_builder(*messages)

            self.send_message(text, blocks)
