from datetime import datetime

import kivy.properties as kp
from kivy.logger import Logger

from data.esports.stats import calculate_teams_damage
from data.events.data_event_dispatch import DataEventDispatcher
from data.esports.stats import convert_milliseconds_to_HMS_string


class GameEventDispatcher(DataEventDispatcher):

    # Input Events
    champ_select_event = kp.DictProperty({})
    game_info_event = kp.DictProperty({})
    pause_started_event = kp.DictProperty({})
    current_stats_update = kp.DictProperty({})
    

    # Output Properties
    game_version = kp.StringProperty()
    number_of_players = kp.NumericProperty(0)
    current_game_time = kp.NumericProperty(0)
    
    tricode_left = kp.StringProperty()
    tricode_right = kp.StringProperty()

    players = kp.DictProperty()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.live_data.bind(champ_select_event=self.setter('champ_select_event'))
        self.app.live_data.bind(game_info_event=self.setter('game_info_event'))
        self.app.live_data.bind(pause_started_event=self.setter('pause_started_event'))
        self.app.livestats_history.bind(current_stats_update=self.setter('current_stats_update'))

        self.set_default_players()

    
    def on_game_info_event(self, *args):

        if (self.number_of_players == 0 and
            "participants" in self.game_info_event
        ):
            self.number_of_players = len(self.game_info_event["participants"])
            self.get_tricodes(self.game_info_event["participants"])
            self.get_player_info(self.game_info_event["participants"])

        if "gameVersion" in self.game_info_event:
            self.game_version = self.game_info_event["gameVersion"]



    def on_latest_stats_update(self, *args):
    
        if ("participants" in self.latest_stats_update and
            self.number_of_players == 0
        ):
            self.number_of_players = len(self.latest_stats_update["participants"])

            if (self.tricode_left == "" or
                self.tricode_right == ""
            ):
                self.get_tricodes(self.latest_stats_update["participants"])

            if len(self.players) == 0:
                self.get_player_info(self.latest_stats_update["participants"])


    def on_current_stats_update(self, *args):

        if "gameTime" in self.current_stats_update:
            self.current_game_time = self.current_stats_update["gameTime"]


    def on_pause_started_event(self, *args):

        if len(self.pause_started_event) > 0:

            LogMessage = (
                f"Game Paused: {datetime.now().strftime('%r')}"
            )

            if "gameTime" in self.pause_started_event:
                game_time = self.pause_started_event["gameTime"]
                game_time_string = datetime.utcfromtimestamp(game_time/1000).strftime("%H:%M:%S")

                LogMessage += f" at gametime: {game_time_string}"

            Logger.info(LogMessage)

   
    def on_game_reset(self, *args):

        self.game_version = ""
        self.number_of_players = 0

        self.tricode_left = "BLUE"
        self.tricode_right = "RED"

        self.set_default_players()


    def get_tricodes(self, participants, *args):

        def get_tricode(participants, teamID):

            tricode = None

            for this_participant in participants:

                if (("summonerName" in this_participant or "playerName" in this_participant) and
                    "teamID" in this_participant and
                    this_participant["teamID"] == teamID
                ):

                    name_array = []

                    if "summonerName" in this_participant:
                        name_array = this_participant["summonerName"].split(" ")

                    elif "playerName" in this_participant:
                        name_array = this_participant["playerName"].split(" ")

                    if len(name_array) > 1:

                        tricode = name_array[0]

                        return tricode

            return tricode

        blue_tricode = get_tricode(participants, 100)
        red_tricode = get_tricode(participants, 200)

        if blue_tricode is not None:
            self.tricode_left = blue_tricode

        if red_tricode is not None:
            self.tricode_right = red_tricode


    def get_player_info(self, participants, *args):

        def get_name(participant):

            name = None
            name_array = []

            if "summonerName" in this_participant:
                name = participant["summonerName"]
                name_array = name.split(" ")

            elif "playerName" in this_participant:
                name = participant["playerName"]
                name_array = name.split(" ")

            if len(name_array) > 1:
                name = " ".join(name_array[1:])

            return name

        for this_participant in participants:

            if (("summonerName" in this_participant or "playerName" in this_participant) and
                "championName" in this_participant and
                "teamID" in this_participant and
                "participantID" in this_participant
            ):

                this_id = this_participant["participantID"]
                this_name = get_name(this_participant)

                self.players[this_id] = {
                    "summonerName": this_name,
                    "teamID": this_participant["teamID"],
                    "championName": this_participant["championName"]
                }



    def set_default_players(self, *args):

        teamID = 100

        for i in range(1, 11):

            if i > 5:
                teamID = 200

            self.players[i] = {
                "summonerName": "",
                "teamID": teamID,
                "championName": "default"
            }
