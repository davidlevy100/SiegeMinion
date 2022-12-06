import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher

class DragonDispatcher(DataEventDispatcher):

    # Input Properties
    monster_event = kp.DictProperty()
    next_dragon_event = kp.DictProperty()


    # Output Properties

    blue_dragons = kp.ListProperty([])
    red_dragons = kp.ListProperty([])

    blue_dragon_map = kp.DictProperty()
    red_dragon_map = kp.DictProperty()

    next_dragon_name = kp.StringProperty("")
    next_dragon_spawn_time = kp.NumericProperty(0)

    last_dragon_killer = kp.NumericProperty(0)

    sequence_index = kp.NumericProperty(0)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.live_data.bind(dragon_event=self.setter('monster_event'))
        self.app.live_data.bind(next_dragon_event=self.setter('next_dragon_event'))
        

    def on_monster_event(self, *args):

        if ("dragonType" in self.monster_event and
            "killerTeamID" in self.monster_event and
            "killer" in self.monster_event and
            "gameTime" in self.monster_event
        ):
            
            dragon = self.monster_event["dragonType"]
            self.last_dragon_killer = self.monster_event["killer"]
            game_time = self.monster_event["gameTime"]

            if self.monster_event["killerTeamID"] == 100:
                self.blue_dragons.append(dragon)
                self.blue_dragon_map[game_time] = dragon
            
            elif self.monster_event["killerTeamID"] == 200:
                self.red_dragons.append(dragon)
                self.red_dragon_map[game_time] = dragon


    def on_next_dragon_event(self, *args):

        if ("nextDragonName" in self.next_dragon_event and
            "nextDragonSpawnTime" in self.next_dragon_event and
            "sequenceIndex" in self.next_dragon_event
        ):

            self.next_dragon_name = self.next_dragon_event["nextDragonName"]
            self.next_dragon_spawn_time = self.next_dragon_event["nextDragonSpawnTime"] * 1000
            self.sequence_index = self.next_dragon_event["sequenceIndex"]
            self.update()


    def on_game_reset(self, *args):

        self.blue_dragons = []
        self.red_dragons = []
        self.next_dragon_name = ""
        self.next_dragon_spawn_time = 0
        self.last_dragon_killer = 0
        self.sequence_index = 0

        self.blue_dragon_map.clear()
        self.red_dragon_map.clear()

        self.update()


    def update(self, *args):

        data = {
            "nextDragonName": self.next_dragon_name,
            "nextDragonSpawnTime": self.next_dragon_spawn_time,
            "sequenceIndex": self.sequence_index
        }

        self.send_data(**data)
