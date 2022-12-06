import kivy.properties as kp
from kivy.logger import Logger

from data.events.current.activatable import L3Activatable


class WholeGameGoldAreaChartL3(L3Activatable):

    current_stats_update = kp.DictProperty()

    start_time = kp.NumericProperty(0)
    end_time = kp.NumericProperty(0)

    chart_data = kp.ListProperty()
    chart_min = kp.NumericProperty(0)
    chart_max = kp.NumericProperty(0)

    gold_history = kp.ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.livestats_history.bind(
            current_stats_update=self.setter('current_stats_update')
        )

        self.gold_history = self.app.gold_tracker.gold_history

        self.graphic_type = "Lower 3rds"
        self.graphic_name = "Whole Game Gold Area Chart"

        self.active_title = self.app.config.getdefault("User Game Data", "whole_game_gold_area_chart_l3_title", "")


    def on_game_reset(self, *args):

        super().on_game_reset(*args)

        self.chart_max = 0
        self.chart_min = 0
        self.chart_data.clear()

        self.active = False

        self.start_time = 0
        self.end_time = 0


    def on_current_stats_update(self, *args):

        if (self.visible or 
            self.active
        ):
            self.update_properties()


    def update_properties(self, *args):

        if ("gameTime" in self.current_stats_update and
            self.current_stats_update["gameTime"] in self.gold_history
        ):

            current_time = self.current_stats_update["gameTime"]
        
            end_index = self.gold_history.index(current_time)
            start_index = 0

            new_data = [
                x["gold_diff"] for x in self.gold_history.values()[start_index:end_index]
            ]

            self.start_time = self.gold_history.keys()[start_index]
            self.end_time = self.gold_history.keys()[end_index]
            
            self.chart_data = new_data

            if len(new_data) > 0:
                self.chart_min = min(new_data)
                self.chart_max = max(new_data)

            else:
                self.chart_min = 0
                self.chart_max = 0
