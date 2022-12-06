import kivy.properties as kp
from kivy.logger import Logger

from data.events.current.activatable import L3Activatable

# length of gold data window
# if not whole game 


class LiveGoldAreaChartL3(L3Activatable):

    gold_history = kp.ObjectProperty()

    live_data_window = kp.NumericProperty(300000)
    mode = kp.OptionProperty(
        "5 Minutes", options=["5 Minutes", "10 Minutes"]
    )
    
    current_stats_update = kp.DictProperty()

    start_time = kp.NumericProperty(0)
    end_time = kp.NumericProperty(0)

    chart_data = kp.ListProperty()
    chart_min = kp.NumericProperty(0)
    chart_max = kp.NumericProperty(0)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.livestats_history.bind(
            current_stats_update=self.setter('current_stats_update')
        )

        self.gold_history = self.app.gold_tracker.gold_history

        self.graphic_type = "Lower 3rds"
        self.graphic_name = "Live Gold Area Chart"

        self.active_title = self.app.config.getdefault("User Game Data", "live_gold_area_chart_l3_title", "")


    def on_mode(self, *args):

        if self.mode == "5 Minutes":
            self.live_data_window = 300000

        elif self.mode == "10 Minutes":
            self.live_data_window = 600000


    def on_game_reset(self, *args):

        super().on_game_reset(*args)

        self.chart_max = 0
        self.chart_min = 0
        self.chart_data.clear()

        self.start_time = 0
        self.end_time = 0
        

    def on_current_stats_update(self, *args):

        if (self.visible or 
            self.active
        ):
            self.update_properties()


    def set_mode(self, new_mode, *args):
        self.mode = new_mode


    def update_properties(self, *args):

        if ("gameTime" in self.current_stats_update and
            self.current_stats_update["gameTime"] in self.gold_history
        ):

            current_time = self.current_stats_update["gameTime"]
        
            end_index = self.gold_history.index(current_time)
            start_index = self.gold_history.bisect_left((current_time - self.live_data_window))

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
