from pprint import pprint as pp

from kivy.clock import Clock
import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher
from data.esports.stats import convert_milliseconds_to_HMS_string

from data.livestats.timed_objectives import INHIBITOR_TIME


class Inhibitor(DataEventDispatcher):

    # Input Properties
    current_stats_update = kp.DictProperty()
    lane_teamID = kp.StringProperty("")
    manual = kp.BooleanProperty()

    # Output Properties
    active = kp.BooleanProperty(True)

    timer = kp.NumericProperty(0)
    timer_string = kp.StringProperty("---")

    run_event = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.livestats_history.bind(
            current_stats_update=self.setter('current_stats_update')
        )


    def on_current_stats_update(self, *args):        

        if (not self.manual and
            "inhibitors" in self.current_stats_update and
            "gameTime" in self.current_stats_update and
            self.lane_teamID in self.current_stats_update["inhibitors"]
        ):

            last_destroyed = self.current_stats_update["inhibitors"][self.lane_teamID]

            if last_destroyed is None:
                self.active = True
                self.timer = 0
                return

            time_delta = self.current_stats_update["gameTime"] - last_destroyed

            if 0 < time_delta < INHIBITOR_TIME:
                self.active = False
                self.timer = INHIBITOR_TIME - time_delta

            else:
                self.active = True
                self.timer = 0


    def on_game_reset(self, *args):
        self.manual = False


    def on_manual(self, *args):

        if self.run_event is not None:
            self.run_event.cancel()
            self.run_event = None

        if self.manual:
            self.active = False
            self.timer = INHIBITOR_TIME
            self.run_event = Clock.schedule_interval(self.manual_update, 1.0)

        else:
            self.on_current_stats_update()


    def on_timer(self, *args):

        if (self.timer == INHIBITOR_TIME or
            self.timer <= 0):

            self.timer_string = "---"

        else:
            self.timer_string = convert_milliseconds_to_HMS_string(self.timer)


    def manual_override(self, state, teamID, *args):

        if state == "normal":
            self.manual = False

        else:
            self.manual = True


    def manual_update(self, *args):

        new_time = self.timer - 1000

        if new_time <= 0:
            self.timer = 0
            self.manual = False

        else:
            self.timer = new_time
