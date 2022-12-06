import kivy.properties as kp
from kivy.logger import Logger

from data.vizrt.vizcrank.sender import VizcrankSender

from data.esports.stats import convert_milliseconds_to_HMS_string
from data.esports.stats import calculate_teams_damage
from data.esports.stats import format_number

DRAGONS = {
    "default": "_Placeholder",
    "air": "Drake_Cloud",
    "fire": "Drake_Infernal",
    "earth": "Drake_Mountain",
    "water": "Drake_Ocean",
    "chemtech": "Drake_Chemtech",
    "hextech": "Drake_Hextech"
}

#Picks - Blue 0111 - 0115 / Red 0211 - 0215
PICK_FIELDS = ["0111", "0112", "0113", "0114", "0115", "0211", "0212", "0213", "0214", "0215"]


class PostGameBreakdownSender(VizcrankSender):

    game_info_event = kp.DictProperty()
    champ_select_event = kp.DictProperty()
    game_end_event = kp.DictProperty()
    latest_stats_update = kp.DictProperty()

    title = kp.ConfigParserProperty(
        "",
        "Post-Game Breakdown",
        "title",
        "app",
        val_type=str
    )
    subtitle = kp.ConfigParserProperty(
        "",
        "Post-Game Breakdown",
        "subtitle",
        "app",
        val_type=str
    )

    graph_x_tick_width = kp.ConfigParserProperty(
        0,
        "Post-Game Breakdown",
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

    pick_champion1 = kp.DictProperty()
    pick_champion2 = kp.DictProperty()
    pick_champion3 = kp.DictProperty()
    pick_champion4 = kp.DictProperty()
    pick_champion5 = kp.DictProperty()
    pick_champion6 = kp.DictProperty()
    pick_champion7 = kp.DictProperty()
    pick_champion8 = kp.DictProperty()
    pick_champion9 = kp.DictProperty()
    pick_champion10 = kp.DictProperty()

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
        
        self.app.live_data.bind(champ_select_event=self.setter('champ_select_event'))
        self.app.live_data.bind(game_end_event=self.setter('game_end_event'))
        self.app.live_data.bind(latest_stats_update=self.setter('latest_stats_update'))
        self.app.live_data.bind(game_info_event=self.setter('game_info_event'))

        self.app.livestats_history.bind(server_time=self.setter('server_time'))

        self.app.overlay_players.player1.bind(pick_champion=self.setter('pick_champion1'))
        self.app.overlay_players.player2.bind(pick_champion=self.setter('pick_champion2'))
        self.app.overlay_players.player3.bind(pick_champion=self.setter('pick_champion3'))
        self.app.overlay_players.player4.bind(pick_champion=self.setter('pick_champion4'))
        self.app.overlay_players.player5.bind(pick_champion=self.setter('pick_champion5'))
        self.app.overlay_players.player6.bind(pick_champion=self.setter('pick_champion6'))
        self.app.overlay_players.player7.bind(pick_champion=self.setter('pick_champion7'))
        self.app.overlay_players.player8.bind(pick_champion=self.setter('pick_champion8'))
        self.app.overlay_players.player9.bind(pick_champion=self.setter('pick_champion9'))
        self.app.overlay_players.player10.bind(pick_champion=self.setter('pick_champion10'))


        self.record_left = self.app.top_bar.record_left
        self.record_right = self.app.top_bar.record_right
        self.app.top_bar.bind(record_left=self.setter('record_left'))
        self.app.top_bar.bind(record_right=self.setter('record_right'))

        self.wins_left = self.app.top_bar.wins_left
        self.wins_right = self.app.top_bar.wins_right
        self.app.top_bar.bind(wins_left=self.setter('wins_left'))
        self.app.top_bar.bind(wins_right=self.setter('wins_right'))


        #Config Keys
        self.section = "Post-Game Breakdown"


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
            game_data["fields"][field]["value"] = self.title

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


        # Wins/Record
        win_or_record = self.app.config.get(
            "User Game Data",
            "win_or_record",
        )

        #Left Team Win/Record
        field = "0102"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = " "

        
        #Right Team Win/Record
        field = "0202"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = " "
                
        
        #Red Team Logo
        field = "0200"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = self.viz_logo_right

        
        #Red Team Tricode
        field = "0201"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = self.tricode_right


        #Picks - Blue 0111 - 0115 / Red 0211 - 0215
        for index, field in enumerate(PICK_FIELDS, 1):

            # Champion Internal Name
            this_pick_champion = self.property(f'pick_champion{index}')
            champion = this_pick_champion.get(self)

            if ("internal_name" in champion and
                self.has_field(field=field, fields=game_data["fields"], key="value")
            ):
                game_data["fields"][field]["value"] = champion["internal_name"]


        # Bans - Blue 0121 - 0125 / Red 0221 - 0225
        if (len(self.champ_select_event) > 0 and
            "bannedChampions" in self.champ_select_event
        ):

            try:

                # Bans - Blue 0121 - 0125
                blue_ban_ids = [x["championID"] for x in self.champ_select_event["bannedChampions"] if x["teamID"] == 100]

                blue_bans = ["_Placeholder"] * 5
                
                for index, this_ban_id in enumerate(blue_ban_ids):
                    champion = self.app.data_dragon.get_asset("champion", f"{this_ban_id}")
                    if champion is not None:
                        blue_bans[index] = champion["internal_name"]

                for index, this_ban in enumerate(blue_bans, 121):
                    field = f"0{index}"
                    if self.has_field(field=field, fields=game_data["fields"], key="value"):
                        game_data["fields"][field]["value"] = this_ban


                # Bans - Red 0221 - 0225
                red_ban_ids = [x["championID"] for x in self.champ_select_event["bannedChampions"] if x["teamID"] == 200]

                red_bans = ["_Placeholder"] * 5

                for index, this_ban_id in enumerate(red_ban_ids):
                    champion = self.app.data_dragon.get_asset("champion", f"{this_ban_id}")
                    if champion is not None:
                        red_bans[index] = champion["internal_name"]

                for index, this_ban in enumerate(red_bans, 221):
                    field = f"0{index}"
                    if self.has_field(field=field, fields=game_data["fields"], key="value"):
                        game_data["fields"][field]["value"] = this_ban

            except Exception as e:
                Logger.exception(f"Error: {e}")

        # K/D/A Blue: 1101 / Red 1102
        for index, this_team in enumerate(self.latest_stats_update["teams"], 1101):
            field = f"{index}"
            if (self.has_field(field=field, fields=game_data["fields"], key="value") and
                "assists" in this_team and
                "championsKills" in this_team and
                "deaths" in this_team
            ):
                k = this_team["championsKills"]
                d = this_team["deaths"]
                a = this_team["assists"]

                game_data["fields"][field]["value"] = f"{k}/{d}/{a}"

        # Gold - Blue: 1201 / Red: 1202
        if len(self.app.gold_tracker.gold_history) > 0:
            last_gold = self.app.gold_tracker.gold_history.values()[-1]

            if "blue_gold" in last_gold:
                field = "1201"
                blue_gold = last_gold["blue_gold"]
                if self.has_field(field=field, fields=game_data["fields"], key="value"):
                    game_data["fields"][field]["value"] = format_number(blue_gold)

            if "red_gold" in last_gold:
                field = "1202"
                red_gold = last_gold["red_gold"]
                if self.has_field(field=field, fields=game_data["fields"], key="value"):
                    game_data["fields"][field]["value"] = format_number(red_gold)

        # Turrets (Towers) - Blue: 1301 / Red: 1302
        for index, this_team in enumerate(self.latest_stats_update["teams"], 1301):
            field = f"{index}"
            if (self.has_field(field=field, fields=game_data["fields"], key="value") and
                "towerKills" in this_team
            ):
                game_data["fields"][field]["value"] = f"{this_team['towerKills']}"

        # Dragons
        # Blue Dragons 1411 - 1414
        blue_dragons = ["_Placeholder"] * 4
        for index, this_dragon in enumerate(self.latest_stats_update["teams"][0]["dragons"]):

            if index < len(blue_dragons):
                blue_dragons[index] = DRAGONS.get(this_dragon, "_Placeholder")

        for index, this_dragon_code in enumerate(blue_dragons, 1411):
            field = f"{index}"
            if self.has_field(field=field, fields=game_data["fields"], key="value"):
                game_data["fields"][field]["value"] = this_dragon_code


        # Red Dragons 1421 - 1424
        red_dragons = ["_Placeholder"] * 4
        for index, this_dragon in enumerate(self.latest_stats_update["teams"][1]["dragons"]):

            if index < len(red_dragons):
                red_dragons[index] = DRAGONS.get(this_dragon, "_Placeholder")

        for index, this_dragon_code in enumerate(red_dragons, 1421):
            field = f"{index}"
            if self.has_field(field=field, fields=game_data["fields"], key="value"):
                game_data["fields"][field]["value"] = this_dragon_code
    

        #Elder Dragons - Blue: 1501 / Red: 1502
        for index, this_team in enumerate(self.latest_stats_update["teams"], 1501):
            field = f"{index}"
            if (self.has_field(field=field, fields=game_data["fields"], key="value") and
                "elderKills" in this_team
            ):
                game_data["fields"][field]["value"] = f"{this_team['elderKills']}"

        #Barons - Blue: 1601 / Red: 1602
        for index, this_team in enumerate(self.latest_stats_update["teams"], 1601):
            field = f"{index}"
            if (self.has_field(field=field, fields=game_data["fields"], key="value") and
                "baronKills" in this_team
            ):
                game_data["fields"][field]["value"] = f"{this_team['baronKills']}"


        ## Gold Graph

        # 7000 Array of numbers separated by |

        gold_data = [x["gold_diff"] for x in self.app.gold_tracker.gold_history.values() if "gold_diff" in x]

        min_gold = 0
        max_gold = 0

        abridged_min = 0
        abridged_max = 0

        if len(gold_data) > 0:
            min_gold = min(gold_data)
            max_gold = max(gold_data)        

        while len(gold_data) > 600:
            gold_data = gold_data[::2]

        if len(gold_data) > 0:
            abridged_min = min(gold_data)
            abridged_max = max(gold_data)

        gold_string_list = [str(x) for x in gold_data]

        viz_gold_data = "|".join(gold_string_list)

        field = "7000"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = viz_gold_data

        #7010 Min Y Value
        field = "7010"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = format_number(min_gold)

        #7013 Max Y Value
        field = "7013"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = format_number(max_gold)

        #7012 Hide Y Zero
        field = "7012"
        hide_zero = "0"
        if min_gold/(min_gold+max_gold) >= 0.01:
            hide_zero="1"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = hide_zero

        #7030 Number of X ticks to show
        field = "7030"
        num_ticks = (self.server_time // 600000) + 1
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = f"{num_ticks}"

        #7031 X Tick Difference
        field = "7031"
        x_tick_diff = (6000000 / self.server_time) * self.graph_x_tick_width
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = f"{x_tick_diff}"


        #7032 Y Position
        field = "7032"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            
            zero_line_y_pos = 50.0

            if abridged_max >= 0 and abridged_min >= 0:
                zero_line_y_pos = 0.0

            elif abridged_max < 0 and abridged_min < 0:
                zero_line_y_pos = 100.0

            else:
                total = abs(abridged_max) + abs(abridged_min)
                zero_line_y_pos = (abs(abridged_min) / total) * 100

            game_data["fields"][field]["value"] = f"{zero_line_y_pos:.4f}"


        #8001 - 8010 / 9001 - 9010 Damage

        if "participants" in self.latest_stats_update:
            damage_list = calculate_teams_damage(self.latest_stats_update["participants"])

        if damage_list is not None:

            for index, this_damage in enumerate(damage_list, 1):
                
                #Raw Numbers
                field = f"{8000 + index}"
                if self.has_field(field=field, fields=game_data["fields"], key="value"):
                    game_data["fields"][field]["value"] = f"{this_damage}"

                #formatted Numbers
                field = f"{9000 + index}"
                if self.has_field(field=field, fields=game_data["fields"], key="value"):
                    game_data["fields"][field]["value"] = format_number(this_damage)

        return game_data
