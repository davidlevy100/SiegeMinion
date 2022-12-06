from datetime import datetime

import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher

DEFAULT_STATE = {
    "blue_turret_kills": 0,
    "red_turret_kills": 0
}


class TurretDispatcher(DataEventDispatcher):

    # Input Properties
    latest_stats_update = kp.DictProperty()
    tower_event = kp.DictProperty()

    blue_turret_kills = set()
    blue_turret_kill_quantity = kp.NumericProperty(0)
    blue_turret_map = kp.DictProperty() 

    red_turret_kills = set()
    red_turret_kill_quantity = kp.NumericProperty(0)
    red_turret_map = kp.DictProperty()



    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.live_data.bind(tower_event=self.setter('tower_event'))
        self.output = DEFAULT_STATE


    def on_tower_event(self, *args):

        if (len(self.tower_event) > 0 and
            "teamID" in self.tower_event and
            "position" in self.tower_event and
            "x" in self.tower_event["position"] and
            "z" in self.tower_event["position"] and
            "gameTime" in self.tower_event
        ):

            this_position = (self.tower_event["position"]["x"], self.tower_event["position"]["z"])
            data = {}

            if self.tower_event["teamID"] == 100:
                owning_team = "Blue "
                self.red_turret_kills.add(this_position)
                self.red_turret_kill_quantity = len(self.red_turret_kills)
                data = {"red_turret_kills": self.red_turret_kill_quantity}

                if this_position not in self.red_turret_map:
                    self.red_turret_map[this_position] = self.tower_event["gameTime"]

                self.send_data(**data)
                
            elif self.tower_event["teamID"] == 200:
                owning_team = "Red "
                self.blue_turret_kills.add(this_position)
                self.blue_turret_kill_quantity = len(self.blue_turret_kills)
                
                data = {"blue_turret_kills": self.blue_turret_kill_quantity}

                if this_position not in self.blue_turret_map:
                    self.blue_turret_map[this_position] = self.tower_event["gameTime"]

                self.send_data(**data)


            if "turretTier" in self.tower_event:
                tier = f"{self.tower_event['turretTier']} "

            if "lane" in self.tower_event:
                lane = f"{self.tower_event['lane']} "

            if "buildingType" in self.tower_event:
                building_type = f"{self.tower_event['buildingType']} "

            if "gameTime" in self.tower_event:
                game_time = self.tower_event["gameTime"]
                game_time_string = datetime.utcfromtimestamp(game_time/1000).strftime("%H:%M:%S")

            LogMessage = (
                f"Game Event: {datetime.now().strftime('%r')} "
                f"{owning_team}{tier}{lane}{building_type}"
                f"destroyed at gametime: {game_time_string}"
            )

            Logger.info(LogMessage)


    def on_game_reset(self, *args):
        self.output = DEFAULT_STATE
        self.blue_turret_kills.clear()
        self.red_turret_kills.clear()
        self.blue_turret_kill_quantity = 0
        self.red_turret_kill_quantity = 0

        self.blue_turret_map.clear()
        self.red_turret_map.clear()
