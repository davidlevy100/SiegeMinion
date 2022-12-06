from datetime import datetime

import kivy.properties as kp

from data.events.data_event_dispatch import DataEventDispatcher


class LCUVizSender(DataEventDispatcher):

    active = kp.BooleanProperty(False)
    active_side = kp.OptionProperty("none", options=["left", "right", "none"])

    reset = kp.StringProperty()

    timer = kp.NumericProperty()
    timer_active = kp.BooleanProperty(False)
    phase_duration = kp.NumericProperty()

    cs_stats_subline = kp.StringProperty()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.vizrt.setter('input_data'))
        self.app.lcu_champ_select.bind(active=self.setter('active'))
        self.app.lcu_champ_select.bind(active_side=self.setter('active_side'))

        self.app.lcu_champ_select.bind(reset=self.setter('reset'))
        self.app.lcu_champ_select.bind(timer=self.setter('timer'))
        self.app.lcu_champ_select.bind(timer_active=self.setter('timer_active'))
        self.app.lcu_champ_select.bind(phase_duration=self.setter('phase_duration'))

        self.cs_stats_subline = self.app.lcu_champ_select.cs_stats_subline
        self.app.lcu_champ_select.bind(cs_stats_subline=self.setter('cs_stats_subline'))

        #Participants
        self.participant1 = LCUParticipantVizSender(index=1, side="left", source=self.app.lcu_champ_select.participant1)
        self.participant2 = LCUParticipantVizSender(index=2, side="left", source=self.app.lcu_champ_select.participant2)
        self.participant3 = LCUParticipantVizSender(index=3, side="left", source=self.app.lcu_champ_select.participant3)
        self.participant4 = LCUParticipantVizSender(index=4, side="left", source=self.app.lcu_champ_select.participant4)
        self.participant5 = LCUParticipantVizSender(index=5, side="left", source=self.app.lcu_champ_select.participant5)
        self.participant6 = LCUParticipantVizSender(index=1, side="right", source=self.app.lcu_champ_select.participant6)
        self.participant7 = LCUParticipantVizSender(index=2, side="right", source=self.app.lcu_champ_select.participant7)
        self.participant8 = LCUParticipantVizSender(index=3, side="right", source=self.app.lcu_champ_select.participant8)
        self.participant9 = LCUParticipantVizSender(index=4, side="right", source=self.app.lcu_champ_select.participant9)
        self.participant10 = LCUParticipantVizSender(index=5, side="right", source=self.app.lcu_champ_select.participant10)

        self.bind(reset=self.participant1.setter('reset'))
        self.bind(reset=self.participant2.setter('reset'))
        self.bind(reset=self.participant3.setter('reset'))
        self.bind(reset=self.participant4.setter('reset'))
        self.bind(reset=self.participant5.setter('reset'))
        self.bind(reset=self.participant6.setter('reset'))
        self.bind(reset=self.participant7.setter('reset'))
        self.bind(reset=self.participant8.setter('reset'))
        self.bind(reset=self.participant9.setter('reset'))
        self.bind(reset=self.participant10.setter('reset'))


    def on_active(self, *args):

        output = {
            "animOn": int(self.active),
            "statSubline": self.cs_stats_subline
        }

        self.app.vizrt.send_now(output)


    def on_active_side(self, *args):

        side_map = {
            "none": 0,
            "left": 1,
            "right": 2
        }

        team = side_map[self.active_side]

        output = {
            "turnSel": team
        }

        self.app.vizrt.send_now(output)


    def on_reset(self, *args):

        output = {
            "LOAD": 1,
            "turnSel": 0,
            "clock": int(self.timer / 1000),
            "phaseDuration": int(self.timer / 1000),
            "clockOff": int(not(self.timer_active)),
            "statSubline": self.cs_stats_subline
        }

        self.app.vizrt.send_now(output)


    def on_timer(self, *args):

        output = {
            "clock": int(self.timer / 1000)
        }

        self.app.vizrt.send_now(output)


    def on_timer_active(self, *args):

        output = {
            "clockOff": int(not(self.timer_active))
        }

        self.app.vizrt.send_now(output)

    
    def on_phase_duration(self, *args):

        output = {
            "phaseDuration": int(self.phase_duration / 1000)
        }

        self.app.vizrt.send_now(output)


class LCUParticipantVizSender(DataEventDispatcher):

    side = kp.OptionProperty("none", options=["left", "right", "none"])
    index = kp.NumericProperty()

    source = kp.ObjectProperty()

    ban_champion = kp.DictProperty()
    pick_champion = kp.DictProperty()
    spell1 = kp.DictProperty()
    spell2 = kp.DictProperty()

    ban_completed = kp.BooleanProperty(False)
    pick_completed = kp.BooleanProperty(False)

    show_stats = kp.BooleanProperty(False)

    pick_rate = kp.StringProperty("")
    ban_rate = kp.StringProperty("")
    win_rate = kp.StringProperty("")

    pick_state = kp.OptionProperty("off", options=["off", "picking", "completed"])
    ban_state = kp.OptionProperty("off", options=["off", "banning", "completed"])

    reset = kp.StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.vizrt.setter('input_data'))

        self.prefix = ""

        if self.side == "left":
            self.prefix = "b"

        elif self.side == "right":
            self.prefix = "r"

        self.source.bind(ban_champion=self.setter('ban_champion'))
        self.source.bind(pick_champion=self.setter('pick_champion'))
        self.source.bind(spell1=self.setter('spell1'))
        self.source.bind(spell2=self.setter('spell2'))
        self.source.bind(ban_completed=self.setter('ban_completed'))
        self.source.bind(pick_completed=self.setter('pick_completed'))
        self.source.bind(show_stats=self.setter('show_stats'))
        self.source.bind(pick_rate=self.setter('pick_rate'))
        self.source.bind(ban_rate=self.setter('ban_rate'))
        self.source.bind(win_rate=self.setter('win_rate'))

        self.source.bind(ban_state=self.setter('ban_state'))
        self.source.bind(pick_state=self.setter('pick_state'))


    def on_reset(self, *args):

        self.output = {}

        output = {
            f"{self.prefix}Ban{self.index}": "_Placeholder",
            f"{self.prefix}pChamp{self.index}": "_Placeholder",
            f"{self.prefix}pChampText{self.index}": "",
            f"{self.prefix}pLock{self.index}": 0,
            f"{self.prefix}p{self.index}ShowStats": 0,
            f"{self.prefix}p{self.index}Stat1": "",
            f"{self.prefix}p{self.index}Stat2": "",
            f"{self.prefix}p{self.index}Stat3": "",
            f"{self.prefix}BanSel{self.index}": 0,
            f"{self.prefix}PickSel{self.index}": 0
        }

        self.app.vizrt.send_now(output)



    def on_ban_champion(self, *args):

        if ("internal_name" in args[1]):

            output = {
                f"{self.prefix}Ban{self.index}": args[1]["internal_name"]
            }

            self.send_data(**output)
    

    def on_pick_champion(self, *args):

        if ("internal_name" in args[1] and
            "external_name" in args[1]
        ):

            output = {
                f"{self.prefix}pChamp{self.index}": args[1]["internal_name"],
                f"{self.prefix}pChampText{self.index}": args[1]["external_name"]
            }
            self.send_data(**output)


    def on_pick_completed(self, *args):

        output = {
            f"{self.prefix}pLock{self.index}": int(self.pick_completed)
        }

        self.send_data(**output)


    def on_show_stats(self, *args):

        output = {
            f"{self.prefix}p{self.index}ShowStats": int(self.show_stats)
        }

        self.send_data(**output)

    
    def on_pick_rate(self, *args):

        output = {
            f"{self.prefix}p{self.index}Stat1": self.pick_rate
        }

        self.send_data(**output)


    def on_ban_rate(self, *args):

        output = {
            f"{self.prefix}p{self.index}Stat2": self.ban_rate
        }

        self.send_data(**output)


    def on_win_rate(self, *args):

        output = {
            f"{self.prefix}p{self.index}Stat3": self.win_rate
        }

        self.send_data(**output)


    def on_ban_state(self, *args):

        ban_map = {
            "off": 0,
            "banning": 1,
            "completed": 2
        }

        ban_state = ban_map[self.ban_state]

        if self.ban_completed:
            ban_state = 2

        output = {
            f"{self.prefix}BanSel{self.index}": ban_state
        }

        self.send_data(**output)


    def on_pick_state(self, *args):


        pick_map = {
            "off": 0,
            "picking": 1,
            "completed": 2,
        }

        pick_state = pick_map[self.pick_state]

        if self.pick_completed:
            pick_state = 2

        output = {
            f"{self.prefix}PickSel{self.index}": pick_state
        }

        self.send_data(**output)
