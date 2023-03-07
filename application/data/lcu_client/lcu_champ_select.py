from datetime import datetime
from itertools import chain

from kivy.clock import Clock
import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher


class LCUChampSelect(DataEventDispatcher):

    champ_select_data = kp.DictProperty()

    active = kp.BooleanProperty(False)
    reset = kp.StringProperty()
    
    timer = kp.NumericProperty()
    timer_active = kp.BooleanProperty(False)

    phase_duration = kp.NumericProperty()


    active_side = kp.OptionProperty("none", options=["left", "right", "none"])
    active_banner = kp.NumericProperty(-1)
    active_picker = kp.NumericProperty(-1)

    active_banners = kp.ListProperty([])
    active_pickers = kp.ListProperty([])

    last_banner = kp.NumericProperty(-1)
    last_picker = kp.NumericProperty(-1)

    run_event = None

    cs_stats_subline = kp.ConfigParserProperty(
        "",
        "User Game Data",
        "cs_stats_subline",
        "app"
    )


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.lcu_poller.bind(output=self.setter('champ_select_data'))

        self.participant1 = LCUParticipant(team_key="myTeam", cell_ID=0)
        self.participant2 = LCUParticipant(team_key="myTeam", cell_ID=1)
        self.participant3 = LCUParticipant(team_key="myTeam", cell_ID=2)
        self.participant4 = LCUParticipant(team_key="myTeam", cell_ID=3)
        self.participant5 = LCUParticipant(team_key="myTeam", cell_ID=4)

        self.participant6 = LCUParticipant(team_key="theirTeam", cell_ID=5)
        self.participant7 = LCUParticipant(team_key="theirTeam", cell_ID=6)
        self.participant8 = LCUParticipant(team_key="theirTeam", cell_ID=7)
        self.participant9 = LCUParticipant(team_key="theirTeam", cell_ID=8)
        self.participant10 = LCUParticipant(team_key="theirTeam", cell_ID=9)

        self.bind(reset=self.participant1.setter('reset'))
        self.bind(active_banner=self.participant1.setter('active_banner'))
        self.bind(active_picker=self.participant1.setter('active_picker'))
        self.participant1.bind(last_banner=self.setter('last_banner'))
        self.participant1.bind(last_picker=self.setter('last_picker'))

        self.bind(reset=self.participant2.setter('reset'))
        self.bind(active_banner=self.participant2.setter('active_banner'))
        self.bind(active_picker=self.participant2.setter('active_picker'))
        self.participant2.bind(last_banner=self.setter('last_banner'))
        self.participant2.bind(last_picker=self.setter('last_picker'))

        self.bind(reset=self.participant3.setter('reset'))
        self.bind(active_banner=self.participant3.setter('active_banner'))
        self.bind(active_picker=self.participant3.setter('active_picker'))
        self.participant3.bind(last_banner=self.setter('last_banner'))
        self.participant3.bind(last_picker=self.setter('last_picker'))

        self.bind(reset=self.participant4.setter('reset'))
        self.bind(active_banner=self.participant4.setter('active_banner'))
        self.bind(active_picker=self.participant4.setter('active_picker'))
        self.participant4.bind(last_banner=self.setter('last_banner'))
        self.participant4.bind(last_picker=self.setter('last_picker'))

        self.bind(reset=self.participant5.setter('reset'))
        self.bind(active_banner=self.participant5.setter('active_banner'))
        self.bind(active_picker=self.participant5.setter('active_picker'))
        self.participant5.bind(last_banner=self.setter('last_banner'))
        self.participant5.bind(last_picker=self.setter('last_picker'))

        self.bind(reset=self.participant6.setter('reset'))
        self.bind(active_banner=self.participant6.setter('active_banner'))
        self.bind(active_picker=self.participant6.setter('active_picker'))
        self.participant6.bind(last_banner=self.setter('last_banner'))
        self.participant6.bind(last_picker=self.setter('last_picker'))

        self.bind(reset=self.participant7.setter('reset'))
        self.bind(active_banner=self.participant7.setter('active_banner'))
        self.bind(active_picker=self.participant7.setter('active_picker'))
        self.participant7.bind(last_banner=self.setter('last_banner'))
        self.participant7.bind(last_picker=self.setter('last_picker'))

        self.bind(reset=self.participant8.setter('reset'))
        self.bind(active_banner=self.participant8.setter('active_banner'))
        self.bind(active_picker=self.participant8.setter('active_picker'))
        self.participant8.bind(last_banner=self.setter('last_banner'))
        self.participant8.bind(last_picker=self.setter('last_picker'))

        self.bind(reset=self.participant9.setter('reset'))
        self.bind(active_banner=self.participant9.setter('active_banner'))
        self.bind(active_picker=self.participant9.setter('active_picker'))
        self.participant9.bind(last_banner=self.setter('last_banner'))
        self.participant9.bind(last_picker=self.setter('last_picker'))

        self.bind(reset=self.participant10.setter('reset'))
        self.bind(active_banner=self.participant10.setter('active_banner'))
        self.bind(active_picker=self.participant10.setter('active_picker'))
        self.participant10.bind(last_banner=self.setter('last_banner'))
        self.participant10.bind(last_picker=self.setter('last_picker'))


    def on_connected(self, *args):

        if (self.connected and
            self.active_banner == -1
        ):
            self.active_banner = 0
        
        elif not self.connected:
            self.active_banner = -1


    def on_game_reset(self, *args):

        self.on_reset()

    
    def on_reset(self, *args):
        self.active = False
        self.phase_duration = 0
        self.timer = 0
        self.timer_active = False
        self.active_side = "none"
        self.active_banner = -1
        self.active_picker = -1


    def on_champ_select_data(self, *args):

        if ("timer" in self.champ_select_data and
            "adjustedTimeLeftInPhase" in self.champ_select_data["timer"] and 
            "totalTimeInPhase" in self.champ_select_data["timer"]
        ): 

            total_time = self.champ_select_data["timer"]["totalTimeInPhase"] // 1000
            adj_time = self.champ_select_data["timer"]["adjustedTimeLeftInPhase"] // 1000

            if total_time - adj_time <= 3:
                self.phase_duration = self.champ_select_data["timer"]["adjustedTimeLeftInPhase"]
                self.timer = self.phase_duration
                self.timer_active = True
                self.start_clock()


        if "actions" in self.champ_select_data:
            self.find_actives(chain(*self.champ_select_data["actions"]))

    def on_last_banner(self, *args):

        self.set_actives("ban", args[1])


    def on_last_picker(self, *args):

        self.set_actives("pick", args[1])


    def start_clock(self, *args):

        if self.run_event is not None:
            self.run_event.cancel()
            
        self.run_event = Clock.schedule_interval(self.update_clock, 1.0)

    
    def stop_clock(self, *args):
        if self.run_event is not None:
            self.run_event.cancel()
            self.run_event = None


    def update_clock(self, *args):

        new_time = self.timer - 1000

        if new_time <= 0:
            self.timer = 0
            self.stop_clock()
        
        else:
            self.timer = new_time


    def set_actives(self, action, cellID):

        action_map = {
            ("ban", 0): ("ban", 5),
            ("ban", 5): ("ban", 1),
            ("ban", 1): ("ban", 6),
            ("ban", 6): ("ban", 2),
            ("ban", 2): ("ban", 7),
            ("ban", 7): ("pick", 0),
            ("pick", 0): ("pick", 5),
            ("pick", 5): ("pick", 6),
            ("pick", 6): ("pick", 1),
            ("pick", 1): ("pick", 2),
            ("pick", 2): ("pick", 7),
            ("pick", 7): ("ban", 8),
            ("ban", 8): ("ban", 3),
            ("ban", 3): ("ban", 9),
            ("ban", 9): ("ban", 4),
            ("ban", 4): ("pick", 8),
            ("pick", 8): ("pick", 3),
            ("pick", 3): ("pick", 4),
            ("pick", 4): ("pick", 9),
        }

        if (action, cellID) in action_map:

            next_action = action_map[(action, cellID)]

            if next_action[0] == "ban":

                self.active_banner = next_action[1]
                self.active_picker = -1
                

            elif next_action[0] == "pick":

                self.active_banner = -1
                self.active_picker = next_action[1]

            else:
                self.active_banner = -1
                self.active_picker = -1

            if (0 <= next_action[1] <= 4):
                self.active_side = "left"

            elif (5 <= next_action[1] <= 9):
                self.active_side = "right"

            else:
                self.active_side = "none"

        else:
            self.active_side = "none"
            self.active_banner = -1
            self.active_picker = -1


    def toggle_active(self, *args):
        self.active = not self.active


    def reset_lcu(self, *args):
        self.reset = str(datetime.now())


    def find_actives(self, actions, *args):

        banning = []
        picking = []

        for this_action in actions:

            if ('actorCellId' in this_action and
                'completed' in this_action and 
                this_action['completed'] is False and
                "isInProgress" in this_action and
                this_action["isInProgress"] is True and
                'type' in this_action
            ):
            
                if this_action['type'] =='ban':
                    banning.append(this_action['actorCellId'])

                elif this_action['type'] =='pick':
                    picking.append(this_action['actorCellId'])

        self.active_banners = banning
        self.active_pickers = picking



class LCUParticipant(DataEventDispatcher):

    reset = kp.StringProperty()

    champ_stats_time = kp.ConfigParserProperty(
        1.0,
        "Sportradar",
        "champion_stats_time",
        "app",
        val_type=float
    )

    champ_select_data = kp.DictProperty()
    picks_bans_wins = kp.DictProperty()

    ban_completed = kp.BooleanProperty(False)
    pick_completed = kp.BooleanProperty(False)
    show_stats = kp.BooleanProperty(False)

    has_stats = kp.BooleanProperty(False)
    pick_rate = kp.StringProperty("")
    ban_rate = kp.StringProperty("")
    win_rate = kp.StringProperty("")

    team_key = kp.StringProperty()
    cell_ID = kp.NumericProperty()

    ban_champion = kp.DictProperty()
    pick_champion = kp.DictProperty()

    spell1 = kp.DictProperty()
    spell2 = kp.DictProperty()

    stat_shutoff = None

    active_picker = kp.NumericProperty(-1)
    active_banner = kp.NumericProperty(-1)
    last_banner = kp.NumericProperty(-1)
    last_picker = kp.NumericProperty(-1)

    pick_state = kp.OptionProperty("off", options=["off", "picking", "completed"])
    ban_state = kp.OptionProperty("off", options=["off", "banning", "completed"])


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.lcu_poller.bind(output=self.setter('champ_select_data'))
        

        self.picks_bans_wins = self.app.sportradar.picks_bans_wins
        self.app.sportradar.bind(picks_bans_wins=self.setter('picks_bans_wins'))

        self.default_champ = self.app.data_dragon.get_asset(
            "champion",
            "default"
        )

        self.default_spell = self.app.data_dragon.get_asset(
            "summoner_spell",
            "default"
        )

        self.on_champ_stats_time()


    def on_active_banner(self, *args):

        if self.ban_completed:
            self.ban_state = "completed"

        else:
            if self.active_banner == self.cell_ID:
                self.ban_state = "banning"

            else:
                self.ban_state = "off"

    
    def on_active_picker(self, *args):

        if (self.active_picker == self.cell_ID and
            self.pick_completed
        ):
            self.pick_state = "completed"

        elif self.active_picker == self.cell_ID:
            self.pick_state = "picking"

        else:
            self.pick_state = "off"



    def on_show_stats(self, *args):

        if self.show_stats:
            self.stat_shutoff()


    def on_champ_stats_time(self, *args):

        if self.stat_shutoff is not None:
            self.stat_shutoff.cancel()

        self.stat_shutoff = Clock.create_trigger(
            self.shutoff_stats,
            self.champ_stats_time
        )


    def on_champ_select_data(self, *args):

        if (not self.pick_completed and
            "actions" in self.champ_select_data
        ):
            self.pick_completed = self.is_pick_completed(
                chain(*self.champ_select_data["actions"])
            )

        # Get Champion Pick
        if self.team_key in self.champ_select_data:
            
            my_data = self.get_my_data(self.champ_select_data[self.team_key])

            if (my_data is not None and
                "championId" in my_data and
                "spell1Id" in my_data and
                "spell2Id" in my_data
            ):
                champ = self.app.data_dragon.get_asset(
                    "champion",
                    str(my_data["championId"])
                )

                if champ is not None:
                    self.pick_champion = champ

                    if self.pick_completed:
                        self.pick_state = "completed"
                    else:
                        self.pick_state = "picking"

                    my_champ = self.pick_champion["external_name"]

                    if (my_champ in self.picks_bans_wins and
                        "Pick Rate" in self.picks_bans_wins[my_champ] and
                        "Ban Rate" in self.picks_bans_wins[my_champ] and
                        "Win Rate" in self.picks_bans_wins[my_champ]
                    ):
                        self.has_stats = True
                        
                        my_stats = self.picks_bans_wins[my_champ]
                    
                        self.pick_rate = f"{float(my_stats['Pick Rate']):.0%}"
                        self.ban_rate = f"{float(my_stats['Ban Rate']):.0%}"
                        self.win_rate = f"{float(my_stats['Win Rate']):.0%}"

                    else:
                        self.has_stats = False

                        self.pick_rate = ""
                        self.ban_rate = ""
                        self.win_rate = ""
                
                else:
                    self.pick_champion = self.default_champ
                    self.has_stats = False
                    self.pick_rate = ""
                    self.ban_rate = ""
                    self.win_rate = ""


                spell1 = self.app.data_dragon.get_asset(
                    "summoner_spell",
                    str(my_data["spell1Id"])
                )

                if spell1 is not None:
                    self.spell1 = spell1

                else:
                    self.spell1 = self.default_spell

                spell2 = self.app.data_dragon.get_asset(
                    "summoner_spell",
                    str(my_data["spell2Id"])
                )

                if spell2 is not None:
                    self.spell2 = spell2

                else:
                    self.spell2 = self.default_spell

        
        if (not self.ban_completed and
            "actions" in self.champ_select_data
        ):
            self.get_ban_data(chain(*self.champ_select_data["actions"]))


    def on_pick_champion(self, *args):
        self.show_stats = False


    def on_game_reset(self, *args):

        self.on_reset()


    def on_reset(self, *args):

        self.ban_champion = self.default_champ
        self.pick_champion = self.default_champ
        self.spell1 = self.default_spell
        self.spell2 = self.default_spell
        
        self.ban_completed = False
        self.pick_completed = False

        self.show_stats = False

        self.has_stats = False
        self.pick_rate = ""
        self.ban_rate = ""
        self.win_rate = ""

        self.last_banner = -1
        self.last_picker = -1

        self.pick_state = "off"
        self.ban_state = "off"


    def on_pick_completed(self, *args):

        if self.pick_completed:
            self.last_picker = self.cell_ID


    def on_ban_completed(self, *args):

        if self.ban_completed:
            self.last_banner = self.cell_ID


    def shutoff_stats(self, *args):

        self.show_stats = False


    def get_my_data(self, team_list, *args):

        for this_player in team_list:

            if ("cellId" in this_player and
                this_player["cellId"] == self.cell_ID
            ):

                return this_player

        return None


    def get_ban_data(self, actions, *args):

        ban_completed = False

        for this_action in actions:

            if ('actorCellId' in this_action and
                this_action['actorCellId'] == self.cell_ID and
                'type' in this_action and
                this_action['type'] == 'ban' and
                'completed' in this_action and 
                this_action['completed'] is True and
                'championId' in this_action
            ):

                champ = self.app.data_dragon.get_asset(
                    "champion",
                    str(this_action["championId"])
                )

                if champ is not None:
                    self.ban_champion = champ
                else:
                    self.ban_champion = self.default_champ

                ban_completed = True

        self.ban_completed = ban_completed


    def is_pick_completed(self, actions):

        for this_action in actions:

            if ('type' in this_action and 
                this_action['type'] == 'pick' and
                'actorCellId' in this_action and
                this_action['actorCellId'] == self.cell_ID and
                'completed' in this_action and 
                this_action['completed'] is True
            ):
                return True

        return False
    

    def toggle_stats(self, *args):

        self.show_stats = not(self.show_stats)
