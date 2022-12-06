from datetime import datetime
import json

import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher
from data.esports.stats import convert_milliseconds_to_HMS_string
from data.esports.stats import format_signed_number
from data.esports.stats import GOLD_DIFF_THRESHOLD

class TopBar(DataEventDispatcher):

    game_version = kp.StringProperty()

    current_stats_update = kp.DictProperty()
    local_time = kp.NumericProperty(0)

    # Output Properties
    active = kp.BooleanProperty(True)
    
    visible = kp.BooleanProperty()

    clock = kp.StringProperty("00:00")

    dragon_left_1 = kp.StringProperty("default")
    dragon_left_2 = kp.StringProperty("default")
    dragon_left_3 = kp.StringProperty("default")
    dragon_left_4 = kp.StringProperty("default")

    dragon_right_1 = kp.StringProperty("default")
    dragon_right_2 = kp.StringProperty("default")
    dragon_right_3 = kp.StringProperty("default")
    dragon_right_4 = kp.StringProperty("default")

    dragon_kills_left = kp.NumericProperty(0)
    dragon_kills_right = kp.NumericProperty(0)

    dragon_soul_active = kp.BooleanProperty(False)
    dragon_soul = kp.StringProperty("default")
    dragon_soul_team = kp.NumericProperty(-1)

    total_gold_left = kp.NumericProperty(0)
    gold_left = kp.StringProperty("")

    gold_diff_left = kp.NumericProperty(0)
    gold_diff_left_str = kp.StringProperty("")

    total_gold_right = kp.NumericProperty(0)
    gold_right = kp.StringProperty("")

    gold_diff_right = kp.NumericProperty(0)
    gold_diff_right_str = kp.StringProperty("")


    kills_left = kp.StringProperty("")
    kills_right = kp.StringProperty("")

    record_left = kp.StringProperty("")
    record_right = kp.StringProperty("")

    towers_left = kp.StringProperty("")
    towers_right = kp.StringProperty("")

    towers_left_mutator = kp.NumericProperty(0)
    towers_right_mutator = kp.NumericProperty(0)

    tricode_left = kp.StringProperty()
    tricode_right = kp.StringProperty()
    

    wins_left = kp.StringProperty("")
    wins_right = kp.StringProperty("")

    last_dragon_killer = kp.NumericProperty(0)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.livestats_history.bind(
            current_stats_update=self.setter('current_stats_update')
        )

        self.app.livestats_history.bind(
            local_time=self.setter('local_time')
        )

        self.app.game_data.bind(tricode_left=self.setter('tricode_left'))
        self.app.game_data.bind(tricode_right=self.setter('tricode_right'))

        self.app.game_data.bind(game_version=self.setter('game_version'))

        self.visible = self.app.config.getboolean("User Game Data", "top_bar")
        self.app.config.add_callback(self.check_visible, "User Game Data", "top_bar")


    def on_game_reset(self, *args):
        self.towers_left_mutator = 0
        self.towers_right_mutator = 0

        self.on_current_stats_update()


    def on_local_time(self, *args):

        self.clock = convert_milliseconds_to_HMS_string(self.local_time)


    def on_current_stats_update(self, *args):

        data = self.current_stats_update

        # Dragons
        for i, this_team in enumerate(data["teams"]):

            if i == 0:
                side = "left"
            else:
                side = "right"

            new_dragons = ["default"] * 4
            dragon_kills = 0

            for j, this_dragon in enumerate(this_team["dragons"]):
                dragon_kills += 1

                if len(new_dragons) > j:
                    new_dragons[j] = this_dragon

            for k, this_dragon in enumerate(new_dragons, 1):
                this_property = self.property(f'dragon_{side}_{k}')
                this_property.set(self, this_dragon)
            
            this_property = self.property(f'dragon_kills_{side}')
            this_property.set(self, dragon_kills)

        if "lastDragonKiller" in data:
            self.last_dragon_killer = data["lastDragonKiller"]


        # Gold

        self.total_gold_left = data["teams"][0]["totalGold"]
        self.gold_left = f'{self.total_gold_left/1000:.1f}k'

        self.total_gold_right = data["teams"][1]["totalGold"]
        self.gold_right = f'{self.total_gold_right/1000:.1f}k'

        self.gold_diff_left = self.total_gold_left-self.total_gold_right
        self.gold_diff_left_str = format_signed_number(self.gold_diff_left)

        self.gold_diff_right = self.total_gold_right-self.total_gold_left
        self.gold_diff_right_str = format_signed_number(self.gold_diff_right)

        
        # Kills
        self.kills_left = f'{data["teams"][0]["championsKills"]}'
        self.kills_right = f'{data["teams"][1]["championsKills"]}'

        # Towers
        self.towers_left = f'{data["towers"]["blue_turret_kills"]}'
        self.towers_right = f'{data["towers"]["red_turret_kills"]}'


    def on_dragon_left_4(self, *args):
        self.update_dragon_soul()

    
    def on_dragon_right_4(self, *args):
        self.update_dragon_soul()
    

    def update_dragon_soul(self, *args):

        if self.dragon_left_4 != "default":
            self.dragon_soul = self.dragon_left_4
            self.dragon_soul_active = True
            self.dragon_soul_team = 100

        elif self.dragon_right_4 != "default":
            self.dragon_soul = self.dragon_right_4
            self.dragon_soul_active = True
            self.dragon_soul_team = 200

        else:
            self.dragon_soul = "default"
            self.dragon_soul_active = False
            self.dragon_soul_team = -1
        

    def update_record(self, side, text):

        if side == "left":
            self.record_left = text

        elif side == "right":
            self.record_right = text


    def update_wins(self, side, number):

        if side == "left":
            self.wins_left = f"{number}"

        elif side == "right":
            self.wins_right = f"{number}"


    def adjust_tower_score(self, side, amount, *args):

        if side == "left":
            self.towers_left_mutator += amount
        
        elif side == "right":
            self.towers_right_mutator += amount


    def set_active(self, state, *args):
        if state == "normal":
            self.active = False
        else:
            self.active = True

        LogMessage = (
            f"Overlay: overlay is {self.active}"
        )
        Logger.info(LogMessage)

    
    def toggle_visible(self, *args):

        self.visible = not(self.visible)

        LogMessage = (
            f"Overlay: Top Bar visible: {self.visible}"
        )
        Logger.info(LogMessage)


    def check_visible(self, *args):
        
        self.visible = self.app.config.getboolean("User Game Data", "top_bar")
