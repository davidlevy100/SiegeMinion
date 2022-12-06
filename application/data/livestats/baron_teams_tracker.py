import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher

class BaronTeamsTrackerDispatcher(DataEventDispatcher):

    team = kp.NumericProperty(0)
    team_index = kp.NumericProperty(0)

    # Input Properties

    gold_diff = kp.NumericProperty(0)
    
    state = kp.OptionProperty(
        "spawning", 
        options=[
            "alive",
            "buff_active",
            "spawning",
            "respawning"
        ]
    )
    baron_team = kp.NumericProperty(0)

    latest_stats_update = kp.DictProperty()
    baron_event = kp.DictProperty()

    inhibitor_event = kp.DictProperty()

    # This is bound in history.py
    total_turret_kill_quantity = kp.NumericProperty(0)


    # my properties
    champion_kills = kp.NumericProperty(0)
    champion_kills_during_BPP = kp.NumericProperty(0)
    baron_kills = kp.NumericProperty(0)
    baron_kill_time = kp.NumericProperty(0)
    gold_diff_history = kp.DictProperty({})
    towers = kp.NumericProperty(0)
    inhibs = kp.NumericProperty(0)

    initial_gold = kp.NumericProperty(0)
    gold = kp.NumericProperty(0)
    gold_history = kp.DictProperty({})
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.live_data.bind(latest_stats_update=self.setter('latest_stats_update'))
        self.app.live_data.bind(inhibitor_event=self.setter('inhibitor_event'))
        self.app.live_data.bind(baron_event=self.setter('baron_event'))


    def on_baron_event(self, *args):

        if ("killerTeamID" in self.baron_event and
            self.baron_event["killerTeamID"] == self.team and
            "gameTime" in self.baron_event
        ):
            game_time = self.baron_event["gameTime"]

            self.baron_kill_time = game_time

            self.gold_diff_history[game_time] = 0
            self.gold_history[game_time] = 0

            self.initial_gold = self.gold


    def on_gold_diff(self, *args):

        if (self.baron_team == self.team and 
            self.state == "buff_active"
        ):
            self.gold_diff_history[self.baron_kill_time] = self.gold_diff


    def on_latest_stats_update(self, *args):

        if ("teams" in self.latest_stats_update and
            len(self.latest_stats_update["teams"]) > self.team_index
        ):

            if "championsKills" in self.latest_stats_update["teams"][self.team_index]:
                old_champ_kills = self.champion_kills
                self.champion_kills = self.latest_stats_update["teams"][self.team_index]["championsKills"]

                if (self.state == "buff_active" and
                    self.baron_team == self.team
                ):
                    self.champion_kills_during_BPP = self.champion_kills_during_BPP + (self.champion_kills - old_champ_kills)


            if "baronKills" in self.latest_stats_update["teams"][self.team_index]:
                self.baron_kills = self.latest_stats_update["teams"][self.team_index]["baronKills"]

            if "totalGold" in self.latest_stats_update["teams"][self.team_index]:
                self.gold = self.latest_stats_update["teams"][self.team_index]["totalGold"]

            if (self.baron_team == self.team and 
                self.state == "buff_active"
            ):
                self.gold_history[self.baron_kill_time] = (self.gold - self.initial_gold)
    

    def on_game_reset(self, *args):

        self.champion_kills = 0
        self.champion_kills_during_BPP = 0
        self.baron_kills = 0
        self.gold_diff_history.clear()
        self.gold_history.clear()
        self.towers = 0
        self.inhibs = 0
        self.initial_gold = 0
        self.gold = 0


    def on_inhibitor_event(self, *args):

        if ("teamID" in self.inhibitor_event and
            self.inhibitor_event["teamID"] != self.team and
            self.baron_team == self.team and
            self.state == "buff_active"
        ):
            self.inhibs = self.inhibs + 1


    def on_total_turret_kill_quantity(self, *args):

        if (self.state == "buff_active" and
            self.baron_team == self.team
        ):
            self.towers = self.towers + 1
