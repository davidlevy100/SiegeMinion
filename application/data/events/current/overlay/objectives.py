from kivy.clock import Clock
import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher
from data.esports.stats import convert_milliseconds_to_HMS_string

from data.livestats.epic_monster import BARON_BUFF_DURATION, ELDER_BUFF_DURATION

from ui.constants.colors import STATUS_OPTIONS


class Objective(DataEventDispatcher):

    # Input Properties
    current_stats_update = kp.DictProperty()    

    # Output Properties
    # active = kp.BooleanProperty(False)

    state = kp.OptionProperty(
        "spawning", 
        options=[
            "alive",
            "buff_active",
            "spawning",
            "respawning"
        ]
    )


    team = kp.StringProperty("")
    teamID = kp.NumericProperty(0)
    buff_timer = kp.NumericProperty(0)
    buff_timer_string = kp.StringProperty("---")

    respawn_timer = kp.NumericProperty(0)
    respawn_timer_string = kp.StringProperty("---")
    
    tricode_left = kp.StringProperty("BLUE")
    tricode_right = kp.StringProperty("RED")

    killer = kp.NumericProperty(0)
    kill_type = kp.StringProperty()

    run_event = None

    objective_time = 0

    status = kp.OptionProperty(
        "good", 
        options=STATUS_OPTIONS
    )

    monster_name = ""


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.livestats_history.bind(
            current_stats_update=self.setter('current_stats_update')
        )

        self.app.game_data.bind(tricode_left=self.setter('tricode_left'))
        self.app.game_data.bind(tricode_right=self.setter('tricode_right'))


    def on_current_stats_update(self, *args):

        if (self.monster_name in self.current_stats_update and
            len(self.current_stats_update[self.monster_name]) > 0 and
            "team" in self.current_stats_update[self.monster_name] and
            "buffTimer" in self.current_stats_update[self.monster_name] and 
            "spawnCountdown" in self.current_stats_update[self.monster_name] and
            "state" in self.current_stats_update[self.monster_name] and
            "killer" in self.current_stats_update[self.monster_name]
        ):
            data = self.current_stats_update[self.monster_name]

            self.state = data["state"]

            self.teamID = data["team"]
            self.buff_timer = data["buffTimer"]

            self.killer = data["killer"]

            self.kill_type = data.get("killType", "")

            if self.buff_timer <= 0:
                self.buff_timer_string = "---"

            else:
                self.buff_timer_string = convert_milliseconds_to_HMS_string(self.buff_timer)

            
            self.respawn_timer = data["spawnCountdown"]

            if self.respawn_timer <= 0:
                self.respawn_timer_string = "---"

            else:
                self.respawn_timer_string = convert_milliseconds_to_HMS_string(self.respawn_timer)

            if self.teamID == 100:
                self.team = self.tricode_left

            elif self.teamID == 200:
                self.team = self.tricode_right
            
            else:
                self.team = ""
        

class ElderDragon(Objective):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.objective_time = ELDER_BUFF_DURATION
        self.monster_name = "elder"


class BaronPowerPlay(Objective):

    gold_string = kp.StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.objective_time = BARON_BUFF_DURATION
        self.monster_name = "baron"


    def on_current_stats_update(self, *args):

        super().on_current_stats_update()

        if ("gold" in self.current_stats_update[self.monster_name]
        ):
            self.gold_string = f'{self.current_stats_update[self.monster_name]["gold"]:+,}'
