import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher
from data.esports.stats import convert_milliseconds_to_HMS_string


STATE_MAP = {
    "alive": "alive",
    "buff_active": "buff_active",
    "spawning": "buff_ended",
    "respawning": "buff_ended"
}


class NextDragon(DataEventDispatcher):

    current_stats_update = kp.DictProperty()

    mode = kp.OptionProperty (
        "next_dragon",
        options=[
            "next_dragon",
            "elder_dragon"
        ]
    )

    next_dragon_name = kp.StringProperty("")
    next_dragon_spawn_time = kp.NumericProperty(0)

    sequence_index = kp.NumericProperty(0)

    dragon_alive = kp.BooleanProperty(False)
    respawn_timer = kp.NumericProperty(0)
    respawn_timer_string = kp.StringProperty("---")

    state = kp.OptionProperty(
        "respawning", 
        options=[
            "alive", # regular dragon is alive
            "buff_active", # elder buff is active
            "buff_ended", # Counting to to next elder dragon 
            "respawning" # Counting to to next dragon (no elders have happened)
        ]
    )

    # Elder Dragon Variables
    elder_dragon = kp.ObjectProperty()
    # elder_active = kp.BooleanProperty()

    elder_state = kp.OptionProperty(
        "spawning", 
        options=[
            "alive", 
            "buff_active", 
            "spawning", 
            "respawning" 
        ]
    )


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.livestats_history.bind(
            current_stats_update=self.setter('current_stats_update')
        )


    def on_game_reset(self, *args):

        self.mode = "next_dragon"


    def on_elder_dragon(self, *args):

        # self.elder_dragon.bind(active=self.setter('elder_active'))
        self.elder_dragon.bind(state=self.setter('elder_state'))


    def on_elder_state(self, *args):
        self.detect_state()


    def on_current_stats_update(self, *args):

        if ("queued_dragon_info" in self.current_stats_update and
            "nextDragonName" in self.current_stats_update["queued_dragon_info"] and
            "nextDragonSpawnTime" in self.current_stats_update["queued_dragon_info"] and
            "sequenceIndex" in self.current_stats_update["queued_dragon_info"] and
            "gameTime" in self.current_stats_update
        ):

            self.next_dragon_name = self.current_stats_update["queued_dragon_info"]["nextDragonName"]
            self.next_dragon_spawn_time = self.current_stats_update["queued_dragon_info"]["nextDragonSpawnTime"]
            self.sequence_index = self.current_stats_update["queued_dragon_info"]["sequenceIndex"]

            game_time = self.current_stats_update["gameTime"]

            timer = self.next_dragon_spawn_time - game_time

            if timer > 0:
                self.respawn_timer = timer
                self.respawn_timer_string = convert_milliseconds_to_HMS_string(timer)

            else:
                self.respawn_timer = 0
                self.respawn_timer_string = "---"

        self.detect_state()


    def detect_state(self, *args):

        # We should be in elder state
        if (self.elder_state in ["alive", "buff_active", "respawning"]
        ):
            self.mode = "elder_dragon"
            self.state = STATE_MAP[self.elder_state]

        else:
            self.mode = "next_dragon"

            if self.respawn_timer > 0:
                self.state = "respawning"
                
            else:
                self.state = "alive"      
