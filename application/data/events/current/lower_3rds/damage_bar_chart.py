from sortedcontainers import SortedList

import kivy.properties as kp
from kivy.logger import Logger

from data.events.current.activatable import L3Activatable
from data.esports.stats import convert_milliseconds_to_HMS_string
from data.esports.stats import calculate_teams_damage


class DamageBarChartL3(L3Activatable):

    # Input Properties
    local_time = kp.NumericProperty(0)
    players = kp.DictProperty()

    start_time = kp.NumericProperty(0)
    end_time = kp.NumericProperty(0)

    # Output Properties
    
    normal_title = kp.StringProperty("")

    whole_game_title = kp.StringProperty("")

    time_window = kp.NumericProperty(0)

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


    ready = kp.BooleanProperty(False)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.game_data.bind(players=self.setter('players'))
        self.app.livestats_history.bind(local_time=self.setter('local_time'))

        self.graphic_type = "Lower 3rds"
        self.graphic_name = "Damage Bar Chart"

        self.get_defaults()


    def on_game_reset(self, *args):

        super().on_game_reset(*args)

        self.get_defaults()

        self.active_title = ""
        self.start_time = 0
        self.end_time = 0

        self.champ_1 = ""
        self.champ_2 = ""
        self.champ_3 = ""
        self.champ_4 = ""
        self.champ_5 = ""
        self.champ_6 = ""
        self.champ_7 = ""
        self.champ_8 = ""
        self.champ_9 = ""
        self.champ_10 = ""

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

        self.ready = False


    def on_start_time(self, *args):

        self.check_ready()


    def on_end_time(self, *args):

        self.check_ready()


    def on_visible(self, *args):

        if self.visible:
            self.set_time(
                (self.local_time - self.time_window * 1000), 
                self.local_time
            )


    def check_ready(self, *args):

        if self.end_time > self.start_time:
            self.ready = True

        else:
            self.ready = False


    def get_defaults(self, *args):

        self.normal_title = self.app.config.getdefault(
            "User Game Data", 
            "damage_chart_l3_title",
            ""
        )

        self.whole_game_title = self.app.config.getdefault(
            "User Game Data", 
            "damage_chart_l3_whole_game_title",
            ""
        )

        self.time_window = self.app.config.getdefaultint(
            "User Game Data", 
            "damage_chart_l3_time_window",
            0
        )


    def set_time(self, start_time, end_time, *args):


        self.active_title = self.normal_title

        self.start_time = max(start_time, 0)
        self.end_time = end_time
        
        self.update_properties()


    def set_whole_game(self, *args):

        self.active_title = self.whole_game_title

        self.start_time = 0
        self.end_time = self.local_time

        self.update_properties()


    def update_title(self, title, *args):
        self.active_title = title


    def update_properties(self, *args):

        if (self.start_time is None or
            self.end_time is None
        ):
            return

        new_data = self.get_sort()

        if (new_data is not None and
            len(new_data) > 0
        ):
            
            max_value = max(new_data)

            if max_value == 0:
                max_value = 1

            for index, this_data in enumerate(new_data, 1):

                this_participant = self.players[index]

                this_champ = self.property(f'champ_{index}')
                this_champ.set(self, this_participant["championName"])

                this_value = self.property(f'value_{index}')
                this_value.set(self, f'{this_data:,}')

                this_percent = self.property(f'percent_{index}')
                this_percent.set(self, this_data/max_value)
        

    def get_sort(self, *args):

        result = None
        
        start_index = self.app.livestats_history.get_history_index(self.start_time)
        end_index = self.app.livestats_history.get_history_index(self.end_time)

        if (start_index is not None and
            end_index is not None
        ):

            if start_index > end_index:
                start_index, end_index = end_index, start_index

            start_data = calculate_teams_damage(
                self.app.livestats_history.stats_update_history.values()[start_index]["participants"]
            )
            end_data = calculate_teams_damage(
                self.app.livestats_history.stats_update_history.values()[end_index]["participants"]
            )

            result = [j - i for i, j in zip(start_data, end_data)]

        return result
