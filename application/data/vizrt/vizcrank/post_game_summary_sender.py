import kivy.properties as kp
from kivy.logger import Logger

from data.vizrt.vizcrank.sender import VizcrankSender

from data.esports.stats import convert_milliseconds_to_HMS_string
from data.esports.stats import calculate_teams_damage
from data.esports.stats import format_number
from data.esports.stats import string_KDA
from data.esports.stats import string_KP


class PostGameSummarySender(VizcrankSender):

    game_info_event = kp.DictProperty()
    champ_select_event = kp.DictProperty()
    game_end_event = kp.DictProperty()
    latest_stats_update = kp.DictProperty()

    title = kp.ConfigParserProperty(
        "",
        "Post-Game Summary",
        "title",
        "app",
        val_type=str
    )
    subtitle = kp.ConfigParserProperty(
        "",
        "Post-Game Summary",
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

        self.record_left = self.app.top_bar.record_left
        self.record_right = self.app.top_bar.record_right
        self.app.top_bar.bind(record_left=self.setter('record_left'))
        self.app.top_bar.bind(record_right=self.setter('record_right'))

        self.wins_left = self.app.top_bar.wins_left
        self.wins_right = self.app.top_bar.wins_right
        self.app.top_bar.bind(wins_left=self.setter('wins_left'))
        self.app.top_bar.bind(wins_right=self.setter('wins_right'))

        self.players = [
            self.app.overlay_players.player1,
            self.app.overlay_players.player2,
            self.app.overlay_players.player3,
            self.app.overlay_players.player4,
            self.app.overlay_players.player5,
            self.app.overlay_players.player6,
            self.app.overlay_players.player7,
            self.app.overlay_players.player8,
            self.app.overlay_players.player9,
            self.app.overlay_players.player10
        ]


        #Config Keys
        self.section = "Post-Game Summary"


    def can_process(self, *args):

        return len(self.game_end_event) > 0


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
                
        
        #Red Team Logo
        field = "0200"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = self.viz_logo_right

        
        #Red Team Tricode
        field = "0201"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = self.tricode_right


        #Right Team Win/Record
        field = "0202"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = " "


        # Team Gold - Blue: 0131 / Red: 0231
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


        # Team Kills: Blue 0141 / Red 0241
        blue_team_kills = None
        red_team_kills = None

        if ("teams" in self.latest_stats_update and
            len(self.latest_stats_update["teams"]) > 1 and
            "championsKills" in self.latest_stats_update["teams"][0] and
            "championsKills" in self.latest_stats_update["teams"][1]
        ):
            blue_team_kills = self.latest_stats_update["teams"][0]["championsKills"]
            red_team_kills = self.latest_stats_update["teams"][1]["championsKills"]

            if self.has_field(field="0141", fields=game_data["fields"], key="value"):
                game_data["fields"]["0141"]["value"] = f"{blue_team_kills}"

            if self.has_field(field="0241", fields=game_data["fields"], key="value"):
                game_data["fields"]["0241"]["value"] = f"{red_team_kills}"


        damage_list = None

        if "participants" in self.latest_stats_update:
            damage_values = calculate_teams_damage(self.latest_stats_update["participants"])

        if (damage_values is not None
            and len(damage_values) == 10
        ):
            damage_list = damage_values
            game_dmg_max = max(damage_list)

        
        #Individual Player Data

        champ_image_index = 1100
        player_name_index = 1110
        kda_index = 2100
        kp_index = 3100
        dmg_pct_index = 4100
        dmg_fmt_index = 5100
        
        for index, this_player in enumerate(self.players, 1):
            
            #Champion Images tabfields 1101-1110
            champion = this_player.pick_champion
            champ_tabfield = f"{champ_image_index+index}"

            if ("internal_name" in champion and
                self.has_field(field=champ_tabfield, fields=game_data["fields"], key="value")
            ):
                game_data["fields"][champ_tabfield]["value"] = champion["internal_name"]


            #Player Name tabfields 1111-1120
            player_name_tabfield = f"{player_name_index+index}"
            
            if self.has_field(field=player_name_tabfield, fields=game_data["fields"], key="value"):
                game_data["fields"][player_name_tabfield]["value"] = this_player.name

            
            #K/D/A tabfields 2101 - 2110
            kda_tabfield = f"{kda_index+index}"
            kda = string_KDA(self.latest_stats_update["participants"][index-1])

            if self.has_field(field=kda_tabfield, fields=game_data["fields"], key="value"):
                game_data["fields"][kda_tabfield]["value"] = kda


            #Kill Participation 3101 - 3110
            kp_tabfield = f"{kp_index+index}"

            team_kills = blue_team_kills

            if index > 5:
                team_kills = red_team_kills

            kp = string_KP(self.latest_stats_update["participants"][index-1], team_kills)
            if self.has_field(field=kp_tabfield, fields=game_data["fields"], key="value"):
                game_data["fields"][kp_tabfield]["value"] = kp


            #Damage
            if damage_list is not None:

                my_dmg = damage_list[index-1]
                my_dmg_pct = my_dmg / game_dmg_max

                # As Percentages 4101 - 4110
                dmg_pct_tabfield = f"{dmg_pct_index+index}"
                if self.has_field(field=kp_tabfield, fields=game_data["fields"], key="value"):
                    game_data["fields"][dmg_pct_tabfield]["value"] = f"{my_dmg_pct:.4}"

                # As Formatted Numbers 5101 - 5110
                dmg_fmt_tabfield = f"{dmg_fmt_index+index}"
                if self.has_field(field=kp_tabfield, fields=game_data["fields"], key="value"):
                    game_data["fields"][dmg_fmt_tabfield]["value"] = format_number(my_dmg)

        return game_data
