from datetime import datetime
from sortedcontainers import SortedList

import kivy.properties as kp
from kivy.logger import Logger

from data.events.current.activatable import SideSlabActivatable
from data.esports.stats import convert_milliseconds_to_HMS_string


LEVELS = {
    1: 0,
    2: 280,
    3: 660,
    4: 1140,
    5: 1720,
    6: 2400,
    7: 3180,
    8: 4060,
    9: 5040,
    10: 6120,
    11: 7300,
    12: 8580,
    13: 9960,
    14: 11440,
    15: 13020,
    16: 14700,
    17: 16480,
    18: 18360 
}

class XPLevelSideSlab(SideSlabActivatable):

    # Input Properties
    current_stats_update = kp.DictProperty()

    players = kp.DictProperty()

    tricode_left = kp.StringProperty()
    tricode_right = kp.StringProperty()

    # Output Properties
    active_title = kp.ConfigParserProperty(
        "",
        "User Game Data",
        "xp_level_side_slab_title",
        "app"
    )

    bar_teamID_1 = kp.NumericProperty(100)
    bar_teamID_2 = kp.NumericProperty(100)
    bar_teamID_3 = kp.NumericProperty(100)
    bar_teamID_4 = kp.NumericProperty(100)
    bar_teamID_5 = kp.NumericProperty(100)
    bar_teamID_6 = kp.NumericProperty(200)
    bar_teamID_7 = kp.NumericProperty(200)
    bar_teamID_8 = kp.NumericProperty(200)
    bar_teamID_9 = kp.NumericProperty(200)
    bar_teamID_10 = kp.NumericProperty(200)

    champ_1 = kp.StringProperty("")
    champ_2 = kp.StringProperty("")
    champ_3 = kp.StringProperty("")
    champ_4 = kp.StringProperty("")
    champ_5 = kp.StringProperty("")
    champ_6 = kp.StringProperty("")
    champ_7 = kp.StringProperty("")
    champ_8 = kp.StringProperty("")
    champ_9 = kp.StringProperty("")
    champ_10 = kp.StringProperty("")

    player_name_1 = kp.StringProperty("")
    player_name_2 = kp.StringProperty("")
    player_name_3 = kp.StringProperty("")
    player_name_4 = kp.StringProperty("")
    player_name_5 = kp.StringProperty("")
    player_name_6 = kp.StringProperty("")
    player_name_7 = kp.StringProperty("")
    player_name_8 = kp.StringProperty("")
    player_name_9 = kp.StringProperty("")
    player_name_10 = kp.StringProperty("")

    value_1 = kp.StringProperty("")
    value_2 = kp.StringProperty("")
    value_3 = kp.StringProperty("")
    value_4 = kp.StringProperty("")
    value_5 = kp.StringProperty("")
    value_6 = kp.StringProperty("")
    value_7 = kp.StringProperty("")
    value_8 = kp.StringProperty("")
    value_9 = kp.StringProperty("")
    value_10 = kp.StringProperty("")

    level_1 = kp.StringProperty("")
    level_2 = kp.StringProperty("")
    level_3 = kp.StringProperty("")
    level_4 = kp.StringProperty("")
    level_5 = kp.StringProperty("")
    level_6 = kp.StringProperty("")
    level_7 = kp.StringProperty("")
    level_8 = kp.StringProperty("")
    level_9 = kp.StringProperty("")
    level_10 = kp.StringProperty("")

    percent_1 = kp.NumericProperty(0)
    percent_2 = kp.NumericProperty(0)
    percent_3 = kp.NumericProperty(0)
    percent_4 = kp.NumericProperty(0)
    percent_5 = kp.NumericProperty(0)
    percent_6 = kp.NumericProperty(0)
    percent_7 = kp.NumericProperty(0)
    percent_8 = kp.NumericProperty(0)
    percent_9 = kp.NumericProperty(0)
    percent_10 = kp.NumericProperty(0)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.livestats_history.bind(
            current_stats_update=self.setter('current_stats_update')
        )

        self.app.game_data.bind(players=self.setter('players'))
        self.app.game_data.bind(tricode_left=self.setter('tricode_left'))
        self.app.game_data.bind(tricode_right=self.setter('tricode_right'))

        self.summoners = {}
        self.champions = {}

        self.graphic_type = "Side Slab"
        self.graphic_name = "XP + Level"


    def on_players(self, *args):
        self.update_properties()

    
    def on_game_reset(self, *args):
        
        super().on_game_reset(*args)

        self.bar_teamID_1 = 100
        self.bar_teamID_2 = 100
        self.bar_teamID_3 = 100
        self.bar_teamID_4 = 100
        self.bar_teamID_5 = 100
        self.bar_teamID_6 = 200
        self.bar_teamID_7 = 200
        self.bar_teamID_8 = 200
        self.bar_teamID_9 = 200
        self.bar_teamID_10 = 200

        self.champ_1 = "default"
        self.champ_2 = "default"
        self.champ_3 = "default"
        self.champ_4 = "default"
        self.champ_5 = "default"
        self.champ_6 = "default"
        self.champ_7 = "default"
        self.champ_8 = "default"
        self.champ_9 = "default"
        self.champ_10 = "default"

        self.player_name_1 = ""
        self.player_name_2 = ""
        self.player_name_3 = ""
        self.player_name_4 = ""
        self.player_name_5 = ""
        self.player_name_6 = ""
        self.player_name_7 = ""
        self.player_name_8 = ""
        self.player_name_9 = ""
        self.player_name_10 = ""

        self.value_1 = ""
        self.value_2 = ""
        self.value_3 = ""
        self.value_4 = ""
        self.value_5 = ""
        self.value_6 = ""
        self.value_7 = ""
        self.value_8 = ""
        self.value_9 = ""
        self.value_10 = ""

        self.level_1 = ""
        self.level_2 = ""
        self.level_3 = ""
        self.level_4 = ""
        self.level_5 = ""
        self.level_6 = ""
        self.level_7 = ""
        self.level_8 = ""
        self.level_9 = ""
        self.level_10 = ""

        self.percent_1 = 0
        self.percent_2 = 0
        self.percent_3 = 0
        self.percent_4 = 0
        self.percent_5 = 0
        self.percent_6 = 0
        self.percent_7 = 0
        self.percent_8 = 0
        self.percent_9 = 0
        self.percent_10 = 0


    def on_current_stats_update(self, *args):

        if (self.visible or 
            self.active
        ):
            self.update_properties()


    def update_properties(self, *args):

        new_sort = self.get_sort()

        if new_sort is not None:

            for index, this_tuple in enumerate(new_sort[::-1], 1):

                this_ID = this_tuple[-1]

                this_participant = self.players[this_ID]

                this_bar_teamID = self.property(f'bar_teamID_{index}')
                this_bar_teamID.set(self, this_participant["teamID"])

                this_champ = self.property(f'champ_{index}')
                this_champ.set(self, this_participant["championName"])

                this_player_name = self.property(f'player_name_{index}')
                this_player_name.set(self, this_participant["summonerName"])

                this_level = self.property(f'level_{index}')
                this_level.set(self, f'{this_tuple[0]:,}')

                this_value = self.property(f'value_{index}')
                this_value.set(self, f'{this_tuple[1]:,}')

                bar_scale = self.get_bar_scale(this_tuple[0], this_tuple[1])

                this_percent = self.property(f'percent_{index}')
                this_percent.set(self, bar_scale)

                self.update_now = str(datetime.now())


    def get_sort(self, *args):

        result = None

        if "participants" in self.current_stats_update:

            new_sort = SortedList(key=lambda a: (a[0], a[1] -a[2]))

            for this_participant in self.current_stats_update["participants"]:

                if ("level" in this_participant and
                    "XP" in this_participant and
                    "participantID" in this_participant
                ):

                    level = this_participant["level"]
                    xp = min(LEVELS[18], this_participant["XP"])
                    ID = this_participant["participantID"]

                    new_sort.add(
                        (level, xp, ID)
                    )

            result = new_sort
        
        return result


    def get_bar_scale(self, level, xp):

        result = 1.0

        if level < 18:

            min_xp = LEVELS[level]
            max_xp = LEVELS[level+1]

            result = (xp - min_xp) / (max_xp - min_xp)

        return result
