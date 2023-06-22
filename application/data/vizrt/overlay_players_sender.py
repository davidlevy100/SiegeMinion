from datetime import datetime

import kivy.properties as kp

from data.events.data_event_dispatch import DataEventDispatcher
from data.vizrt.viz_helper import get_passive_image


class AllPlayersVizSender(DataEventDispatcher):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.player1 = PlayerVizSender(source=self.app.overlay_players.player1, participant_ID=1)
        self.player2 = PlayerVizSender(source=self.app.overlay_players.player2, participant_ID=2)
        self.player3 = PlayerVizSender(source=self.app.overlay_players.player3, participant_ID=3)
        self.player4 = PlayerVizSender(source=self.app.overlay_players.player4, participant_ID=4)
        self.player5 = PlayerVizSender(source=self.app.overlay_players.player5, participant_ID=5)
        self.player6 = PlayerVizSender(source=self.app.overlay_players.player6, participant_ID=6)
        self.player7 = PlayerVizSender(source=self.app.overlay_players.player7, participant_ID=7)
        self.player8 = PlayerVizSender(source=self.app.overlay_players.player8, participant_ID=8)
        self.player9 = PlayerVizSender(source=self.app.overlay_players.player9, participant_ID=9)
        self.player10 = PlayerVizSender(source=self.app.overlay_players.player10, participant_ID=10)


class PlayerVizSender(DataEventDispatcher):

    local_time = kp.NumericProperty(0)
    
    participant_ID = kp.NumericProperty()

    pick_champion = kp.DictProperty()

    source = kp.ObjectProperty()
    stacks = kp.NumericProperty(-1)
    didStack = kp.BooleanProperty(False)

    cat1 = kp.StringProperty("")
    cat2 = kp.StringProperty("")
    cat3 = kp.StringProperty("")

    stat1 = kp.StringProperty("")
    stat2 = kp.StringProperty("")
    stat3 = kp.StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.vizrt.setter('input_data'))

        self.app.livestats_history.bind(local_time=self.setter('local_time'))

        self.stacks = self.source.stacks
        self.source.bind(stacks=self.setter('stacks'))
        self.source.bind(pick_champion=self.setter('pick_champion'))
        self.source.bind(didStack=self.setter('didStack'))

        self.source.bind(cat1=self.setter('cat1'))
        self.source.bind(cat2=self.setter('cat2'))
        self.source.bind(cat3=self.setter('cat3'))

        self.source.bind(stat1=self.setter('stat1'))
        self.source.bind(stat2=self.setter('stat2'))
        self.source.bind(stat3=self.setter('stat3'))


    def on_local_time(self, *args):
        self.update_stats()

    
    def on_stacks(self, *args):

        champ = self.pick_champion.get("internal_name", "_blank")
        passive = get_passive_image(champ)
        stacks = self.stacks

        if (champ == "Syndra" and
            self.didStack and 
            self.stacks == -1
            ):
            passive = get_passive_image("Syndra2")
            stacks = " "

        if (champ == "Draven" and
            self.didStack and 
            self.stacks == -1
            ):
            stacks = 0

        output = {
            f"players/p{self.participant_ID}/stacks": stacks,
            f"players/p{self.participant_ID}/passive": passive
        }

        self.send_data(**output)



    def update_stats(self, *args):

        output = {
            f"statbox/p{self.participant_ID}/cat1": self.cat1,
            f"statbox/p{self.participant_ID}/stat1": self.stat1,
            f"statbox/p{self.participant_ID}/cat2": self.cat2,
            f"statbox/p{self.participant_ID}/stat2": self.stat2,
            f"statbox/p{self.participant_ID}/cat3": self.cat3,
            f"statbox/p{self.participant_ID}/stat3": self.stat3
        }

        self.send_data(**output)
        