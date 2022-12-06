import math
from string import Template

import kivy.properties as kp
from kivy.logger import Logger

from data.vizrt.vizcrank.sender import VizcrankSender

from data.esports.stats import convert_milliseconds_to_HMS_string
from data.esports.stats import format_number, format_signed_number

CHART_MULTIPLE = 2000

class PostGameObjectivesSender(VizcrankSender):

    game_info_event = kp.DictProperty()
    champ_select_event = kp.DictProperty()
    game_end_event = kp.DictProperty()
    latest_stats_update = kp.DictProperty()

    title = kp.ConfigParserProperty(
        "",
        "Post-Game Objectives",
        "title",
        "app",
        val_type=str
    )
    subtitle = kp.ConfigParserProperty(
        "",
        "Post-Game Objectives",
        "subtitle",
        "app",
        val_type=str
    )

    graph_x_tick_width = kp.ConfigParserProperty(
        0,
        "Post-Game Objectives",
        "graph_x_tick_width",
        "app",
        val_type=float
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

    blue_turret_map = kp.DictProperty()
    red_turret_map = kp.DictProperty()

    blue_inhib_kills = kp.ListProperty()
    red_inhib_kills = kp.ListProperty()

    blue_dragon_map = kp.DictProperty()
    red_dragon_map = kp.DictProperty()

    elder_kill_history = kp.DictProperty()
    baron_kill_history = kp.DictProperty()
    rift_herald_kill_history = kp.DictProperty()

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

        self.app.livestats_history.towers.bind(blue_turret_map=self.setter('blue_turret_map'))
        self.app.livestats_history.towers.bind(red_turret_map=self.setter('red_turret_map'))

        self.app.livestats_history.inhibs.bind(blue_inhib_kills=self.setter('blue_inhib_kills'))
        self.app.livestats_history.inhibs.bind(red_inhib_kills=self.setter('red_inhib_kills'))

        self.app.livestats_history.dragons.bind(blue_dragon_map=self.setter('blue_dragon_map'))
        self.app.livestats_history.dragons.bind(red_dragon_map=self.setter('red_dragon_map'))

        self.app.livestats_history.elder.bind(kill_history=self.setter('elder_kill_history'))
        self.app.livestats_history.baron.bind(kill_history=self.setter('baron_kill_history'))
        self.app.livestats_history.rift_herald.bind(kill_history=self.setter('rift_herald_kill_history'))

        self.record_left = self.app.top_bar.record_left
        self.record_right = self.app.top_bar.record_right
        self.app.top_bar.bind(record_left=self.setter('record_left'))
        self.app.top_bar.bind(record_right=self.setter('record_right'))

        self.wins_left = self.app.top_bar.wins_left
        self.wins_right = self.app.top_bar.wins_right
        self.app.top_bar.bind(wins_left=self.setter('wins_left'))
        self.app.top_bar.bind(wins_right=self.setter('wins_right'))


        #Config Keys
        self.section = "Post-Game Objectives"

        
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


        # Objectives Data

        ## Blue Turrets
        field = "6001"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            blue_turret_list = []
            blue_turret_string = ""
            
            blue_turret_list = [f"{x/self.server_time:.4}" for x in list(self.blue_turret_map.values())[::2]]
            blue_turret_string = "|".join(blue_turret_list)

            game_data["fields"][field]["value"] = blue_turret_string

        ## Blue Turrets
        field = "6002"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            blue_turret_list = []
            blue_turret_string = ""
            
            blue_turret_list = [f"{x/self.server_time:.4}" for x in list(self.blue_turret_map.values())[1::2]]
            blue_turret_string = "|".join(blue_turret_list)

            game_data["fields"][field]["value"] = blue_turret_string


        ## Red Turrets
        field = "7001"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            red_turret_list = []
            red_turret_string = ""
            
            red_turret_list = [f"{x/self.server_time:.4}" for x in list(self.red_turret_map.values())[::2]]
            red_turret_string = "|".join(red_turret_list)

            game_data["fields"][field]["value"] = red_turret_string


        ## Red Turrets
        field = "7002"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            red_turret_list = []
            red_turret_string = ""
            
            red_turret_list = [f"{x/self.server_time:.4}" for x in list(self.red_turret_map.values())[1::2]]
            red_turret_string = "|".join(red_turret_list)

            game_data["fields"][field]["value"] = red_turret_string


        ## Inhibs

        blue_inhibs_matrix = split_list(self.blue_inhib_kills, 10000)
        red_inhibs_matrix = split_list(self.red_inhib_kills, 10000)

        ## Blue Inhibs
        field = "6011"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            blue_inhib_list = []
            blue_inhib_string = ""
            
            blue_inhib_list = [f"{x[0]/self.server_time:.4}" for x in blue_inhibs_matrix if len(x)==1]
            blue_inhib_string = "|".join(blue_inhib_list)

            game_data["fields"][field]["value"] = blue_inhib_string

        field = "6012"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            blue_inhib_list = []
            blue_inhib_string = ""
            
            blue_inhib_list = [f"{(sum(x)/len(x))/self.server_time:.4}" for x in blue_inhibs_matrix if len(x)==2]
            blue_inhib_string = "|".join(blue_inhib_list)

            game_data["fields"][field]["value"] = blue_inhib_string

        ## Red Inhibs
        field = "7011"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            red_inhib_list = []
            red_inhib_string = ""
            
            red_inhib_list = [f"{x[0]/self.server_time:.4}" for x in red_inhibs_matrix if len(x)==1]
            red_inhib_string = "|".join(red_inhib_list)

            game_data["fields"][field]["value"] = red_inhib_string


        ## Red Inhibs
        field = "7012"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            red_inhib_list = []
            red_inhib_string = ""
            
            red_inhib_list = [f"{(sum(x)/len(x))/self.server_time:.4}" for x in red_inhibs_matrix if len(x)==2]
            red_inhib_string = "|".join(red_inhib_list)

            game_data["fields"][field]["value"] = red_inhib_string


        ## Blue Cloud Dragons
        field = "6021"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            dragon_list = []
            dragon_string = ""

            dragon_list = [f"{k/self.server_time:.4}" for k, v in self.blue_dragon_map.items() if v == 'air']
            dragon_string = "|".join(dragon_list)

            game_data["fields"][field]["value"] = dragon_string

        ## Red Cloud Dragons
        field = "7021"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            dragon_list = []
            dragon_string = ""

            dragon_list = [f"{k/self.server_time:.4}" for k, v in self.red_dragon_map.items() if v == 'air']
            dragon_string = "|".join(dragon_list)

            game_data["fields"][field]["value"] = dragon_string

        ## Blue Fire Dragons
        field = "6022"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            dragon_list = []
            dragon_string = ""

            dragon_list = [f"{k/self.server_time:.4}" for k, v in self.blue_dragon_map.items() if v == 'fire']
            dragon_string = "|".join(dragon_list)

            game_data["fields"][field]["value"] = dragon_string

        ## Red Fire Dragons
        field = "7022"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            dragon_list = []
            dragon_string = ""

            dragon_list = [f"{k/self.server_time:.4}" for k, v in self.red_dragon_map.items() if v == 'fire']
            dragon_string = "|".join(dragon_list)

            game_data["fields"][field]["value"] = dragon_string

        ## Blue Mountain Dragons
        field = "6023"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            dragon_list = []
            dragon_string = ""

            dragon_list = [f"{k/self.server_time:.4}" for k, v in self.blue_dragon_map.items() if v == 'earth']
            dragon_string = "|".join(dragon_list)

            game_data["fields"][field]["value"] = dragon_string

        ## Red Mountain Dragons
        field = "7023"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            dragon_list = []
            dragon_string = ""

            dragon_list = [f"{k/self.server_time:.4}" for k, v in self.red_dragon_map.items() if v == 'earth']
            dragon_string = "|".join(dragon_list)

            game_data["fields"][field]["value"] = dragon_string

        ## Blue Ocean Dragons
        field = "6024"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            dragon_list = []
            dragon_string = ""

            dragon_list = [f"{k/self.server_time:.4}" for k, v in self.blue_dragon_map.items() if v == 'water']
            dragon_string = "|".join(dragon_list)

            game_data["fields"][field]["value"] = dragon_string

        ## Red Cloud Dragons
        field = "7024"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            dragon_list = []
            dragon_string = ""

            dragon_list = [f"{k/self.server_time:.4}" for k, v in self.red_dragon_map.items() if v == 'water']
            dragon_string = "|".join(dragon_list)

            game_data["fields"][field]["value"] = dragon_string

        ## Blue Hextech Dragons
        field = "6026"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            dragon_list = []
            dragon_string = ""

            dragon_list = [f"{k/self.server_time:.4}" for k, v in self.blue_dragon_map.items() if v == 'hextech']
            dragon_string = "|".join(dragon_list)

            game_data["fields"][field]["value"] = dragon_string

        ## Red Hextech Dragons
        field = "7026"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            dragon_list = []
            dragon_string = ""

            dragon_list = [f"{k/self.server_time:.4}" for k, v in self.red_dragon_map.items() if v == 'hextech']
            dragon_string = "|".join(dragon_list)

            game_data["fields"][field]["value"] = dragon_string

        
        ## Blue Elder Dragons
        field = "6027"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            dragon_list = []
            dragon_string = ""

            dragon_list = [f"{k/self.server_time:.4}" for k, v in self.elder_kill_history.items() if v == 100]
            dragon_string = "|".join(dragon_list)

            game_data["fields"][field]["value"] = dragon_string

        ## Red Elder Dragons
        field = "7027"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            dragon_list = []
            dragon_string = ""

            dragon_list = [f"{k/self.server_time:.4}" for k, v in self.elder_kill_history.items() if v == 200]
            dragon_string = "|".join(dragon_list)

            game_data["fields"][field]["value"] = dragon_string


        ## Blue Rift Heralds
        field = "6030"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            dragon_list = []
            dragon_string = ""

            dragon_list = [f"{k/self.server_time:.4}" for k, v in self.rift_herald_kill_history.items() if v == 100]
            dragon_string = "|".join(dragon_list)

            game_data["fields"][field]["value"] = dragon_string


        ## Blue Barons
        field = "6031"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            dragon_list = []
            dragon_string = ""

            dragon_list = [f"{k/self.server_time:.4}" for k, v in self.baron_kill_history.items() if v == 100]
            dragon_string = "|".join(dragon_list)

            game_data["fields"][field]["value"] = dragon_string


        ## Red Rift Heralds
        field = "7030"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            dragon_list = []
            dragon_string = ""

            dragon_list = [f"{k/self.server_time:.4}" for k, v in self.rift_herald_kill_history.items() if v == 200]
            dragon_string = "|".join(dragon_list)

            game_data["fields"][field]["value"] = dragon_string


        ## Red Barons
        field = "7031"
        if (self.has_field(field=field, fields=game_data["fields"], key="value")):

            dragon_list = []
            dragon_string = ""

            dragon_list = [f"{k/self.server_time:.4}" for k, v in self.baron_kill_history.items() if v == 200]
            dragon_string = "|".join(dragon_list)

            game_data["fields"][field]["value"] = dragon_string


        #8000 Time Separation
        field = "8000"
        x_tick_diff = (6000000 / self.server_time) * self.graph_x_tick_width
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = f"{x_tick_diff}"


        #8001 Number of X ticks to show
        field = "8001"
        num_ticks = (self.server_time // 300000) + 1
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = f"{num_ticks}"

        return game_data


def split_list(list, delta):

    result = []
    bin = []

    for this_element in list:
        if len(bin) == 0:
            bin.append(this_element)

        elif this_element - bin[-1] > delta:
            result.append(bin.copy())
            bin.clear()
            bin.append(this_element)
        else:
            bin.append(this_element)

    if len(bin) > 0:
        result.append(bin)

    return result
