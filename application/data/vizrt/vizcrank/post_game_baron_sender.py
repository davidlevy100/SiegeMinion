import math
from string import Template

import kivy.properties as kp
from kivy.logger import Logger

from data.vizrt.vizcrank.sender import VizcrankSender

from data.esports.stats import convert_milliseconds_to_HMS_string
from data.esports.stats import format_number, format_signed_number

CHART_MULTIPLE = 2000

class PostGameBaronSender(VizcrankSender):

    game_info_event = kp.DictProperty()
    champ_select_event = kp.DictProperty()
    game_end_event = kp.DictProperty()
    latest_stats_update = kp.DictProperty()

    title = kp.ConfigParserProperty(
        "",
        "Post-Game Baron",
        "title",
        "app",
        val_type=str
    )
    subtitle = kp.ConfigParserProperty(
        "",
        "Post-Game Baron",
        "subtitle",
        "app",
        val_type=str
    )

    tricode_left = kp.StringProperty()
    tricode_right = kp.StringProperty()

    viz_logo_left = kp.StringProperty()
    viz_logo_right = kp.StringProperty()

    winner = kp.OptionProperty(0, options=[0, 1])

    server_time = kp.NumericProperty(0)


    #Specific to this template

    record_left = kp.StringProperty()
    record_right = kp.StringProperty()

    wins_left = kp.StringProperty()
    wins_right = kp.StringProperty()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.game_data.bind(tricode_left=self.setter('tricode_left'))
        self.app.game_data.bind(tricode_right=self.setter('tricode_right'))

        self.viz_logo_left = self.app.viz_mutator.viz_logo_left
        self.app.viz_mutator.bind(viz_logo_left=self.setter('viz_logo_left'))

        self.viz_logo_right = self.app.viz_mutator.viz_logo_right
        self.app.viz_mutator.bind(viz_logo_right=self.setter('viz_logo_right'))
        
        self.app.live_data.bind(game_end_event=self.setter('game_end_event'))
        self.app.live_data.bind(latest_stats_update=self.setter('latest_stats_update'))

        self.app.livestats_history.bind(server_time=self.setter('server_time'))

        self.record_left = self.app.top_bar.record_left
        self.record_right = self.app.top_bar.record_right
        self.app.top_bar.bind(record_left=self.setter('record_left'))
        self.app.top_bar.bind(record_right=self.setter('record_right'))

        self.wins_left = self.app.top_bar.wins_left
        self.wins_right = self.app.top_bar.wins_right
        self.app.top_bar.bind(wins_left=self.setter('wins_left'))
        self.app.top_bar.bind(wins_right=self.setter('wins_right'))


        #Config Keys
        self.section = "Post-Game Baron"

        
    def can_process(self, *args):

        if len(self.game_end_event) == 0:
            return False

        else:
            return True


    def on_game_end_event(self, *args):

        if not self.can_process():
            return

        if not (self.auto_slack or self.auto_trio):
            return
        
        if self.auto_slack:
            self.send_to_slack()

        if self.auto_trio:
            self.send_to_trio()


    def process_game_data(self, game_data, *args):

        #Winner        
        field = "0009"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):

            if "winningTeam" in self.game_end_event:

                if self.game_end_event["winningTeam"] == 100:
                    self.winner = 0

                else:
                    self.winner = 1

            game_data["fields"][field]["value"] = f"{self.winner}"

        # Game Clock
        field = "0010"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_time_string = convert_milliseconds_to_HMS_string(self.server_time)
            game_data["fields"][field]["value"] = game_time_string

        #Title
        field = "0050"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            
            try:
                new_title = Template(self.title).safe_substitute(
                    left_tricode=self.tricode_left, 
                    right_tricode=self.tricode_right
                )

            except Exception as e:
                Logger.exception(e)
                new_title = self.title

            game_data["fields"][field]["value"] = new_title


        #Subtitle
        field = "0051"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = self.subtitle


        #Blue Team Logo
        field = "0100"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = self.viz_logo_left

        
        #Blue Team Tricode
        field = "0101"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = self.tricode_left
                
        
        #Red Team Logo
        field = "0200"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = self.viz_logo_right

        
        #Red Team Tricode
        field = "0201"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = self.tricode_right


        # Wins/Record
        win_or_record = self.app.config.get(
            "User Game Data",
            "win_or_record",
        )

        #Left Team Win/Record
        field = "0102"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):

            blue_result = ""

            if win_or_record == "Record":
                blue_result = f'{self.record_left}'
            
            else:
                blue_result = f'{self.wins_left}'

            game_data["fields"][field]["value"] = blue_result

        
        #Right Team Win/Record
        field = "0202"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):

            red_result = ""

            if win_or_record == "Record":
                red_result = f'{self.record_right}'
            
            else:
                red_result = f'{self.wins_right}'

            game_data["fields"][field]["value"] = red_result


        # Gold - Blue: 0131 / Red: 0231
        if len(self.app.gold_tracker.gold_history) > 0:
            last_gold = self.app.gold_tracker.gold_history.values()[-1]

            if "blue_gold" in last_gold:
                field = "0131"
                blue_gold = last_gold["blue_gold"]
                if self.has_field(field=field, fields=game_data["fields"], key="value"):
                    game_data["fields"][field]["value"] = format_number(blue_gold)

            if "red_gold" in last_gold:
                field = "0231"
                red_gold = last_gold["red_gold"]
                if self.has_field(field=field, fields=game_data["fields"], key="value"):
                    game_data["fields"][field]["value"] = format_number(red_gold)


        # Kills Blue: 0141 / Red 0241
        for index, this_team in enumerate(self.latest_stats_update["teams"], 1):
            field = f"0{index}41"
            if (self.has_field(field=field, fields=game_data["fields"], key="value") and
                "championsKills" in this_team
            ):
                game_data["fields"][field]["value"] = f'{this_team["championsKills"]}'


        # Baron Data
        baron = self.app.livestats_history.baron

        ## Barons Killed:  Blue 1001 / Red 1002
        field = "1001"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = f'{baron.blue_baron_team.baron_kills}'

        field = "1002"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = f'{baron.red_baron_team.baron_kills}'


        ## Baron Gold Diff Sum:  Blue 1003 / Red 1004
        field = "1003"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            blue_bpp_gold = sum(baron.blue_baron_team.gold_diff_history.values())
            game_data["fields"][field]["value"] = format_signed_number(blue_bpp_gold)

            

        field = "1004"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            red_bpp_gold = sum(baron.red_baron_team.gold_diff_history.values())
            game_data["fields"][field]["value"] = format_signed_number(red_bpp_gold)


        ## Champs killed during BPP:  Blue 1005 / Red 1006
        field = "1005"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = f'{baron.blue_baron_team.champion_kills_during_BPP}'

        field = "1006"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = f'{baron.red_baron_team.champion_kills_during_BPP}'


        ## Towers taken during BPP:  Blue 1007 / Red 1008
        field = "1007"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = f'{baron.blue_baron_team.towers}'

        field = "1008"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = f'{baron.red_baron_team.towers}'


        ## Inhibs taken during BPP:  Blue 1009 / Red 1010
        field = "1009"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = f'{baron.blue_baron_team.inhibs}'

        field = "1010"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = f'{baron.red_baron_team.inhibs}'


        ##
        blue_baron_gold = sum(baron.blue_baron_team.gold_history.values())
        red_baron_gold = sum(baron.red_baron_team.gold_history.values())

        gold_max = max(blue_baron_gold, red_baron_gold)
        if gold_max == 0:
            gold_max = 1

        chart_max = math.ceil(gold_max / CHART_MULTIPLE) * CHART_MULTIPLE

        field = "2001"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = f"{blue_baron_gold / chart_max}"

        field = "2002"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = format_number(blue_baron_gold)

        field = "3001"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = f"{red_baron_gold / chart_max}"

        field = "3002"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = format_number(red_baron_gold)

        field = "5001"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = format_number(chart_max)

        return game_data
