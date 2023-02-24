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

    def get_gold_at_game_time(self, game_time):
        """Provides a safe way to get the gold details at a given game time

        Returns gold dict if found, otherwise returns same dict with all values set to 0
        Expects game_time as a time in ms, matching live stats game time
        """

        if game_time in self.gold_history:
            return self.gold_history[game_time]

        return {
            "blue_gold": 0,
            "red_gold": 0,
            "gold_diff": 0
        }

    def on_game_reset(self, *args):
        self.gold_history.clear()
