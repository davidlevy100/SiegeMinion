from datetime import datetime

import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher
from data.esports.stats import convert_milliseconds_to_HMS_string

from data.livestats.baron_teams_tracker import BaronTeamsTrackerDispatcher

# How long the Buff lasts
BARON_BUFF_DURATION = 180000
ELDER_BUFF_DURATION = 150000

# Initial Spawn times
INIT_BARON_RESPAWN_TIME = 1200000
INIT_ELDER_RESPAWN_TIME = 9999999

# How long it takes to respawn
BARON_RESPAWN_DURATION = 360000
ELDER_RESPAWN_DURATION = 360000


class EpicMonsterDispatcher(DataEventDispatcher):

    # Input Properties
    latest_stats_update = kp.DictProperty()
    monster_event = kp.DictProperty()

    # Output Properties

    buffed_players = kp.ListProperty([])
    buff_timer = kp.NumericProperty(0)
    next_spawn_time = kp.NumericProperty(0)
    spawn_countdown = kp.NumericProperty(0)
    state = kp.OptionProperty(
        "spawning", 
        options=[
            "alive",
            "buff_active",
            "spawning",
            "respawning"
        ]
    )
    team = kp.NumericProperty(0)

    blue_kills = kp.NumericProperty(0)
    red_kills = kp.NumericProperty(0)

    killer = kp.NumericProperty(0)
    kill_type = kp.StringProperty()

    # Duration of buff
    buff_duration = 0

    # Game Time when current buff will end
    buff_end_time = 0
    
    # Time of initial spawn
    init_spawn_time = 0

    # respawn time
    respawn_duration = 0

    monster_name = ""

    needs_reset = False

    kill_history = kp.DictProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.live_data.bind(latest_stats_update=self.setter('latest_stats_update'))


    def on_latest_stats_update(self, *args):

        self.update_buff_status()
        self.update_respawn()            
        self.update()

        if self.needs_reset:
            self.reset_buff()


    def on_monster_event(self, *args):

        if ("killerTeamID" in self.monster_event and
            "killer" in self.monster_event and
            "gameTime" in self.monster_event and 
            "participants" in self.latest_stats_update
        ):

            game_time = self.monster_event["gameTime"]

            self.buff_end_time = game_time + self.buff_duration
            self.buff_timer = self.buff_duration

            self.next_spawn_time = game_time + self.respawn_duration
            self.spawn_countdown = self.respawn_duration
            
            self.state = "buff_active"
            self.team = self.monster_event["killerTeamID"]
            self.killer = self.monster_event["killer"]
            self.kill_type = self.monster_event.get("killType", "")

            self.kill_history[game_time] = self.monster_event["killerTeamID"]

            if self.team == 100:
                self.blue_kills = self.blue_kills + 1

            else:
                self.red_kills = self.red_kills + 1

            self.buffed_players = self.get_player_state(
                self.latest_stats_update["participants"],
                self.monster_event["killerTeamID"],
                True
            )

            hms = convert_milliseconds_to_HMS_string(game_time)

            LogMessage = (
                f"{self.monster_name} Kill: " 
                f"at gametime: {hms}"
            )
            Logger.info(LogMessage)


    def on_game_reset(self, *args):

        self.buffed_players = []
        self.buff_timer = 0
        self.next_spawn_time = self.init_spawn_time
        self.spawn_countdown = self.init_spawn_time
        self.state = "spawning"
        self.team = 0
        self.blue_kills = 0
        self.red_kills = 0
        self.killer = 0
        self.kill_type = ""
        self.needs_reset = False
        self.kill_history.clear()


    def reset_buff(self, *args):

        self.buffed_players = []
        self.buff_timer = 0
        self.team = 0
        self.state = "respawning"
        self.killer = 0
        self.kill_type = ""
        self.needs_reset = False


    def update(self, *args):

        data = {
            "buffedPlayers": self.buffed_players,
            "buffTimer": self.buff_timer,
            "killer": self.killer,
            "killType": self.kill_type,
            "spawnCountdown": self.spawn_countdown,
            "state": self.state,
            "team": self.team
        }

        self.send_data(**data)   


    def update_buff_status(self, *args):
        if ("gameTime" in self.latest_stats_update and
            "participants" in self.latest_stats_update and
            self.state == "buff_active"
        ):
            game_time = self.latest_stats_update["gameTime"]
            self.buff_timer = max((self.buff_end_time - game_time), 0)

            # End buff if timer is up
            if game_time > self.buff_end_time:

                hms = convert_milliseconds_to_HMS_string(game_time)

                LogMessage = (
                    f"{self.monster_name} Buff End: Buff timer ended " 
                    f"at gametime: {hms}"
                )
                Logger.info(LogMessage)
                self.needs_reset = True
                return

            # Remove players from buff list if dead
            dead_players = self.get_player_state(
                self.latest_stats_update["participants"],
                self.team,
                False
            )

            current_buffed_players = self.buffed_players[:]

            for this_player in dead_players:
                if this_player in current_buffed_players:
                    current_buffed_players.remove(this_player)

            self.buffed_players = current_buffed_players

            if len(self.buffed_players) < 1:

                hms = convert_milliseconds_to_HMS_string(game_time)

                LogMessage = (
                    f"{self.monster_name} Buff End: All players dead " 
                    f"at gametime: {hms}"
                )
                Logger.info(LogMessage)

                self.needs_reset = True
            

    def get_player_state(self, participants, teamID, is_alive, *args):

        result = []

        for this_participant in participants:

            if ("alive" in this_participant and
                this_participant["alive"] == is_alive and
                "participantID" in this_participant and
                "teamID" in this_participant and
                this_participant["teamID"] == teamID
            ):
                result.append(this_participant["participantID"])

        return result


    def update_respawn(self, *args):

        if ("gameTime" in self.latest_stats_update
        ):

            game_time = self.latest_stats_update["gameTime"]

            if game_time >= self.next_spawn_time:
                self.state = "alive"

            else:
                self.spawn_countdown = self.next_spawn_time - game_time


class ElderDispatcher(EpicMonsterDispatcher):

    next_dragon_event = kp.DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app.live_data.bind(elder_event=self.setter('monster_event'))
        self.app.live_data.bind(next_dragon_event=self.setter('next_dragon_event'))

        self.buff_duration = ELDER_BUFF_DURATION
        self.init_spawn_time = INIT_ELDER_RESPAWN_TIME
        self.respawn_duration = ELDER_RESPAWN_DURATION

        self.monster_name = "Elder"
        
        self.update()


    def on_next_dragon_event(self, *args):

        if ("gameTime" in self.next_dragon_event and
            "nextDragonName" in self.next_dragon_event and
            self.next_dragon_event["nextDragonName"] == "elder" and
            "nextDragonSpawnTime" in self.next_dragon_event
        ):

            self.next_spawn_time = self.next_dragon_event["nextDragonSpawnTime"] * 1000
            self.update_respawn()
            self.update()


class BaronDispatcher(EpicMonsterDispatcher):

    gold_diff = kp.NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.live_data.bind(baron_event=self.setter('monster_event'))

        self.buff_duration = BARON_BUFF_DURATION
        self.init_spawn_time = INIT_BARON_RESPAWN_TIME
        self.respawn_duration = BARON_RESPAWN_DURATION

        self.monster_name = "Baron"

        self.blue_baron_team = BaronTeamsTrackerDispatcher(
            team = 100,
            team_index = 0
        )

        self.bind(gold_diff=self.blue_baron_team.setter("gold_diff"))
        self.bind(state=self.blue_baron_team.setter("state"))
        self.bind(team=self.blue_baron_team.setter("baron_team"))


        self.red_baron_team = BaronTeamsTrackerDispatcher(
            team = 200,
            team_index = 1
        )

        self.bind(gold_diff=self.red_baron_team.setter("gold_diff"))
        self.bind(state=self.red_baron_team.setter("state"))
        self.bind(team=self.red_baron_team.setter("baron_team"))
        
        self.update()

    
    def on_game_reset(self, *args):

        super().on_game_reset()
        self.gold_diff = 0

    
    def on_monster_event(self, *args):

        super().on_monster_event()

        self.initial_gold_diff = self.get_gold_diff(self.team)
        self.gold_diff = 0


    def reset_buff(self, *args):

        super().reset_buff()
        self.gold_diff = 0


    def get_gold_diff(self, team):

        gold_diff = 0

        if ("teams" in self.latest_stats_update and
            len(self.latest_stats_update["teams"]) > 1 and
            "totalGold" in self.latest_stats_update["teams"][0] and
            "totalGold" in self.latest_stats_update["teams"][1]
        ):
            blue_gold = self.latest_stats_update["teams"][0]["totalGold"]
            red_gold = self.latest_stats_update["teams"][1]["totalGold"]
            
            if team == 100:
                gold_diff = blue_gold - red_gold

            else:
                gold_diff = red_gold - blue_gold

        return gold_diff


    def update(self, *args):

        data = {
            "buffedPlayers": self.buffed_players,
            "buffTimer": self.buff_timer,
            "gold": self.gold_diff,
            "killer": self.killer,
            "killType": self.kill_type,
            "spawnCountdown": self.spawn_countdown,
            "state": self.state,
            "team": self.team
        }

        self.send_data(**data)


    def update_buff_status(self, *args):

        super().update_buff_status()

        if ("gameTime" in self.latest_stats_update and
            "participants" in self.latest_stats_update and
            self.state == "buff_active"
        ):

            new_gold_diff = self.get_gold_diff(self.team)
            self.gold_diff = new_gold_diff - self.initial_gold_diff

        else:
            self.gold_diff = 0


class RiftHeraldDispatcher(DataEventDispatcher):

    rift_herald_event = kp.DictProperty()

    teamID = kp.NumericProperty(0)
    killerID = kp.NumericProperty(0)

    sequence_index = kp.NumericProperty(0)

    kill_history = kp.DictProperty()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.live_data.bind(rift_herald_event=self.setter('rift_herald_event'))


    def on_game_reset(self, *args):

        self.teamID = 0
        self.killerID = 0
        self.sequence_index = 0
        self.kill_history.clear()

        self.update()

    def on_rift_herald_event(self, *args):

        if ("killerTeamID" in self.rift_herald_event and
            "killer" in self.rift_herald_event and
            "gameTime" in self.rift_herald_event and
            "sequenceIndex" in self.rift_herald_event
        ):

            self.teamID = self.rift_herald_event["killerTeamID"]
            self.killerID = self.rift_herald_event["killer"]
            self.sequence_index = self.rift_herald_event["sequenceIndex"]

            game_time = self.rift_herald_event["gameTime"]

            self.kill_history[game_time] = self.rift_herald_event["killerTeamID"]

            self.update()

            hms = convert_milliseconds_to_HMS_string(game_time)

            LogMessage = (
                f"Rift Herald Kill: by team {self.teamID} " 
                f"at gametime: {hms}"
            )
            Logger.info(LogMessage)

    def update(self, *args):

        data = {
            "killerTeamID": self.teamID,
            "killer": self.killerID,
            "sequenceIndex": self.sequence_index
        }

        self.send_data(**data)
