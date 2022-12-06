from sortedcontainers import SortedDict

from kivy.app import App
from kivy.clock import Clock
import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher
from data.esports.stats import convert_milliseconds_to_HMS_string
from data.livestats.defaults.stats_update import get_default_stats_update

from data.livestats.epic_monster import ElderDispatcher
from data.livestats.epic_monster import BaronDispatcher
from data.livestats.epic_monster import RiftHeraldDispatcher
from data.livestats.dragon import DragonDispatcher
from data.livestats.timed_objectives import InhibitorsDispatcher
from data.livestats.turrets import TurretDispatcher
from data.livestats.champion_kill_special import SpecialKillDispatcher

DEFAULT_STATS_UPDATE = get_default_stats_update()


from kivy.config import ConfigParser


class LivestatsHistory(DataEventDispatcher):

    correction_factor = kp.ConfigParserProperty(
        1.0,
        "Livestats",
        "correction_factor",
        "app",
        val_type=float
    )

    latest_stats_update = kp.DictProperty()
    current_stats_update = kp.DictProperty()

    server_time = kp.NumericProperty(0)
    local_time = kp.NumericProperty(0)

    delay = kp.ConfigParserProperty(
        0,
        "Livestats",
        "delay",
        "app",
        val_type=int
    )

    paused = kp.BooleanProperty(True)

    elder_output = kp.DictProperty()

    baron_output = kp.DictProperty()

    rift_herald_output = kp.DictProperty()

    blue_dragons = kp.ListProperty()
    red_dragons = kp.ListProperty()
    dragons_output = kp.DictProperty()

    towers_output = kp.DictProperty()
    inhibs_output = kp.DictProperty()

    special_kills_output = kp.DictProperty()

    run_event = None

    sync_server_enabled = kp.BooleanProperty(False)
    sync_server_time = kp.NumericProperty(0)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.live_data.bind(
            latest_stats_update=self.setter('latest_stats_update')
        )

        self.sync_server_enabled = self.app.sync_poller.enabled
        self.app.sync_poller.bind(enabled=self.setter('sync_server_enabled'))

        self.sync_server_time = self.app.sync_poller.server_time
        self.app.sync_poller.bind(server_time=self.setter('sync_server_time'))

        self.app.sync_poller.paused = self.paused
        self.bind(paused=self.app.sync_poller.setter('paused'))

        self.stats_update_history = SortedDict()
        self.stats_update_history[0] = DEFAULT_STATS_UPDATE

        self.elder = ElderDispatcher()
        self.elder.bind(output=self.setter('elder_output'))

        self.baron = BaronDispatcher()
        self.baron.bind(output=self.setter('baron_output'))

        self.rift_herald = RiftHeraldDispatcher()
        self.rift_herald.bind(output=self.setter('rift_herald_output'))

        self.dragons = DragonDispatcher()
        self.dragons.bind(blue_dragons=self.setter('blue_dragons'))
        self.dragons.bind(red_dragons=self.setter('red_dragons'))
        self.dragons.bind(output=self.setter('dragons_output'))

        self.towers = TurretDispatcher()
        self.towers_output = self.towers.output
        self.towers.bind(output=self.setter('towers_output'))

        self.inhibs = InhibitorsDispatcher()
        self.inhibs_output = self.inhibs.output
        self.inhibs.bind(output=self.setter('inhibs_output'))

        self.special_kills = SpecialKillDispatcher()
        self.special_kills.bind(output=self.setter('special_kills_output'))

        self.towers.bind(blue_turret_kill_quantity=self.baron.blue_baron_team.setter("total_turret_kill_quantity"))
        self.towers.bind(red_turret_kill_quantity=self.baron.red_baron_team.setter("total_turret_kill_quantity"))


    def on_game_reset(self, *args):

        self.paused = True

        if self.run_event is not None:
            self.run_event.cancel()
            self.run_event = None
        
        self.stats_update_history.clear()
        self.stats_update_history[0] = DEFAULT_STATS_UPDATE
        self.current_stats_update = DEFAULT_STATS_UPDATE

        self.server_time = 0
        self.local_time = 0


    def on_latest_stats_update(self, *args):

        if ("gameTime" in self.latest_stats_update and
            "teams" in self.latest_stats_update
        ):
            new_update = self.latest_stats_update.copy()

            # Dragons
            new_update["teams"][0]["dragons"] = self.blue_dragons
            new_update["teams"][1]["dragons"] = self.red_dragons
            new_update["queued_dragon_info"] = self.dragons_output
            new_update["lastDragonKiller"] = self.dragons.last_dragon_killer

            # Elder
            new_update["elder"] = self.elder_output
            new_update["teams"][0]["elderKills"] = self.elder.blue_kills
            new_update["teams"][1]["elderKills"] = self.elder.red_kills

            #Rift Herald
            new_update["riftHerald"] = self.rift_herald_output

            # Baron
            new_update["baron"] = self.baron_output

            #Inhibitors
            new_update["inhibitors"] = self.inhibs_output

            #Towers
            new_update["towers"] = self.towers_output

            #Special Kills
            new_update["champion_kill_special"] = self.special_kills_output

            game_time = self.latest_stats_update["gameTime"]

            self.server_time = game_time
            self.stats_update_history[game_time] = new_update


    def on_paused(self, *args):

        if self.paused:
            if self.run_event is not None:
                self.run_event.cancel()
                self.run_event = None
        else:
            if self.run_event is not None:
                self.run_event.cancel()
            self.run_event = Clock.schedule_interval(self.update_time, self.correction_factor)


    def update_time(self, *args):

        if self.sync_server_enabled:
            self.local_time = self.sync_server_time
        else:

            self.local_time = self.local_time + 1000
        
        self.update_current_stats(self.local_time)


    def update_current_stats(self, milliseconds, *args):

        time_index = self.stats_update_history.bisect_left(milliseconds)

        if time_index < len(self.stats_update_history):
            key, value = self.stats_update_history.peekitem(time_index)
        else:
            key, value = self.stats_update_history.peekitem(-1)

        self.current_stats_update = value


    def set_delay(self, milliseconds, *args):

        if self.server_time - milliseconds >= 0:
            self.delay = milliseconds
            
            new_time = round((self.server_time - milliseconds) // 1000) * 1000
            self.local_time = new_time
            self.update_current_stats(new_time)
            self.paused = False


    def goto_time(self, milliseconds, *args):

        if (0 <= milliseconds <= self.server_time):

            self.local_time = milliseconds
            self.update_current_stats(milliseconds)
            self.paused = False


    def bump_time(self, milliseconds, *args):

        new_time = self.local_time + milliseconds

        if 0 <= new_time <= self.server_time:
            self.local_time = new_time
            self.update_current_stats(new_time)


    def get_history_index(self, time, *args):

        """ given 'time' in milliseconds (int), will return and index
            to use in self.stats_update_history
            returns None if not found or time is not an integer
        """

        if (isinstance(time, int) and
            (0 <= time <= self.server_time)
        ):
            return self.stats_update_history.bisect_left(time)
        else:
            return None

    
    def pause_updates(self, *args):

        self.paused = not self.paused
