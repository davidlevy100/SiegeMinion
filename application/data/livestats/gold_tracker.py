from sortedcontainers import SortedDict

import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher


class GoldTracker(DataEventDispatcher):

    latest_stats_update = kp.DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.latest_stats_update = self.app.live_data.latest_stats_update
        self.app.live_data.bind(latest_stats_update=self.setter('latest_stats_update'))

        self.gold_history = SortedDict()


    def on_latest_stats_update(self, *args):

        if ("gameTime" in self.latest_stats_update and
            "teams" in self.latest_stats_update and
            len(self.latest_stats_update["teams"]) > 1 and
            "totalGold" in self.latest_stats_update["teams"][0] and
            "totalGold" in self.latest_stats_update["teams"][1]
        ):

            game_time = self.latest_stats_update["gameTime"]

            blue_total_gold = self.latest_stats_update["teams"][0]["totalGold"]
            red_total_gold = self.latest_stats_update["teams"][1]["totalGold"]

            gold_diff = blue_total_gold - red_total_gold

            self.gold_history[game_time] = {
                "blue_gold": blue_total_gold,
                "red_gold": red_total_gold,
                "gold_diff": gold_diff
            }

    def on_game_reset(self, *args):
        self.gold_history.clear()
