from string import Template

import kivy.properties as kp
from kivy.logger import Logger

from data.vizrt.vizcrank.sender import VizcrankSender

from data.esports.stats import convert_milliseconds_to_HMS_string
from data.esports.stats import format_number



class PostGameGoldSender(VizcrankSender):

    game_info_event = kp.DictProperty()
    champ_select_event = kp.DictProperty()
    game_end_event = kp.DictProperty()
    latest_stats_update = kp.DictProperty()

    title = kp.ConfigParserProperty(
        "",
        "Post-Game Gold",
        "title",
        "app",
        val_type=str
    )
    subtitle = kp.ConfigParserProperty(
        "",
        "Post-Game Gold",
        "subtitle",
        "app",
        val_type=str
    )

    graph_x_tick_width = kp.ConfigParserProperty(
        0,
        "Post-Game Gold",
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
        self.section = "Post-Game Gold"


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


        return game_data
