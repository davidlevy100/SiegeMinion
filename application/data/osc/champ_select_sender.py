from datetime import datetime

from kivy.clock import Clock
import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher


class LCUOSCSender(DataEventDispatcher):

    active = kp.BooleanProperty(False)
    active_side = kp.OptionProperty("none", options=["left", "right", "none"])

    reset = kp.StringProperty()

    timer = kp.NumericProperty()
    timer_active = kp.BooleanProperty(False)
    phase_duration = kp.NumericProperty()

    connected = kp.BooleanProperty(False)
    update = kp.StringProperty("")

    run_event = None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.osc.setter('input_data'))

        self.app.lcu_poller.bind(connected=self.setter('connected'))

        self.app.lcu_champ_select.bind(active=self.setter('active'))
        self.app.lcu_champ_select.bind(active_side=self.setter('active_side'))
        self.app.lcu_champ_select.bind(reset=self.setter('reset'))
        self.app.lcu_champ_select.bind(timer=self.setter('timer'))
        self.app.lcu_champ_select.bind(timer_active=self.setter('timer_active'))
        self.app.lcu_champ_select.bind(phase_duration=self.setter('phase_duration'))


        #Participants
        self.participant1 = LCUParticipantOSCSender(index=1, side="left", source=self.app.lcu_champ_select.participant1)
        self.participant2 = LCUParticipantOSCSender(index=2, side="left", source=self.app.lcu_champ_select.participant2)
        self.participant3 = LCUParticipantOSCSender(index=3, side="left", source=self.app.lcu_champ_select.participant3)
        self.participant4 = LCUParticipantOSCSender(index=4, side="left", source=self.app.lcu_champ_select.participant4)
        self.participant5 = LCUParticipantOSCSender(index=5, side="left", source=self.app.lcu_champ_select.participant5)
        self.participant6 = LCUParticipantOSCSender(index=6, side="right", source=self.app.lcu_champ_select.participant6)
        self.participant7 = LCUParticipantOSCSender(index=7, side="right", source=self.app.lcu_champ_select.participant7)
        self.participant8 = LCUParticipantOSCSender(index=8, side="right", source=self.app.lcu_champ_select.participant8)
        self.participant9 = LCUParticipantOSCSender(index=9, side="right", source=self.app.lcu_champ_select.participant9)
        self.participant10 = LCUParticipantOSCSender(index=10, side="right", source=self.app.lcu_champ_select.participant10)

        self.bind(update=self.participant1.setter('update'))
        self.bind(update=self.participant2.setter('update'))
        self.bind(update=self.participant3.setter('update'))
        self.bind(update=self.participant4.setter('update'))
        self.bind(update=self.participant5.setter('update'))
        self.bind(update=self.participant6.setter('update'))
        self.bind(update=self.participant7.setter('update'))
        self.bind(update=self.participant8.setter('update'))
        self.bind(update=self.participant9.setter('update'))
        self.bind(update=self.participant10.setter('update'))


    def on_active_side(self, *args):

        side_map = {
            "none": 0,
            "left": 1,
            "right": 2
        }

        team = side_map[self.active_side]

        output = {
            "/ChampionSelect/Side": team
        }

        self.send_data(**output)



    def on_connected(self, *args):

        if self.run_event is not None:
            self.run_event.cancel()
            self.run_event = None

        if self.connected:
            self.run_event = Clock.schedule_interval(self.tick, 1.0)


    def tick(self, *args):
        self.update = f"{datetime.now()}"


class LCUParticipantOSCSender(DataEventDispatcher):

    side = kp.OptionProperty("none", options=["left", "right", "none"])
    index = kp.NumericProperty()

    update = kp.StringProperty("")

    source = kp.ObjectProperty()

    ban_champion = kp.DictProperty()
    pick_champion = kp.DictProperty()
    spell1 = kp.DictProperty()
    spell2 = kp.DictProperty()

    pick_completed = kp.BooleanProperty(False)
    show_stats = kp.BooleanProperty(False)

    pick_rate = kp.StringProperty("")
    ban_rate = kp.StringProperty("")
    win_rate = kp.StringProperty("")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.osc.setter('input_data'))

        self.prefix = ""

        if self.side == "left":
            self.prefix = "b"

        elif self.side == "right":
            self.prefix = "r"

        self.source.bind(ban_champion=self.setter('ban_champion'))
        self.source.bind(pick_champion=self.setter('pick_champion'))
        self.source.bind(pick_completed=self.setter('pick_completed'))


    def on_ban_champion(self, *args):

        code = -1

        if ("code" in self.ban_champion
        ):
            code = int(self.ban_champion["code"])  

        output = {
            f"/ChampionSelect/Ban{self.index}": code
        }

        self.send_data(**output)


    def on_pick_champion(self, *args):

        code = -1

        if ("code" in self.pick_champion and
            self.pick_completed
        ):
            code = int(self.pick_champion["code"])  

        output = {
            f"/ChampionSelect/Player{self.index}": code,
            f"/ChampionSelect/Lock{self.index}": int(self.pick_completed)
        }

        self.send_data(**output)


    def on_pick_completed(self, *args):
        self.on_pick_champion()


    def on_update(self, *args):
        self.on_ban_champion()
        self.on_pick_champion()
