import kivy.properties as kp

from data.events.data_event_dispatch import DataEventDispatcher

class OverlayRunesVizSender(DataEventDispatcher):

    # Input Properties
    runes_available = kp.BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.vizrt.setter('input_data'))

        self.active = self.app.overlay_players.runes_available
        self.app.overlay_players.bind(runes_available=self.setter('runes_available'))

        self.player1 = OverlayPlayerRunesVizSender(source=self.app.overlay_players.player1, dp_key="runes/blue1s")
        self.player2 = OverlayPlayerRunesVizSender(source=self.app.overlay_players.player2, dp_key="runes/blue2s")
        self.player3 = OverlayPlayerRunesVizSender(source=self.app.overlay_players.player3, dp_key="runes/blue3s")
        self.player4 = OverlayPlayerRunesVizSender(source=self.app.overlay_players.player4, dp_key="runes/blue4s")
        self.player5 = OverlayPlayerRunesVizSender(source=self.app.overlay_players.player5, dp_key="runes/blue5s")
        self.player6 = OverlayPlayerRunesVizSender(source=self.app.overlay_players.player6, dp_key="runes/red1s")
        self.player7 = OverlayPlayerRunesVizSender(source=self.app.overlay_players.player7, dp_key="runes/red2s")
        self.player8 = OverlayPlayerRunesVizSender(source=self.app.overlay_players.player8, dp_key="runes/red3s")
        self.player9 = OverlayPlayerRunesVizSender(source=self.app.overlay_players.player9, dp_key="runes/red4s")
        self.player10 = OverlayPlayerRunesVizSender(source=self.app.overlay_players.player10, dp_key="runes/red5s")


    def on_game_reset(self, *args):

        output = {
            "runes/off": int(self.active)
        }

        self.app.vizrt.send_now(output)


    def on_runes_available(self, *args):

        output = {
            "runes/off": int(self.runes_available)
        }

        self.send_data(**output)


class OverlayPlayerRunesVizSender(DataEventDispatcher):

    source = kp.ObjectProperty()
    dp_key = kp.StringProperty("")

    secondary_tree = kp.DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def on_source(self, *args):

        self.source.bind(secondary_tree=self.setter('secondary_tree'))


    def on_game_reset(self, *args):

        output = {
            self.dp_key: self.secondary_tree["long_name"]
        }

        self.app.vizrt.send_now(output)

    def on_secondary_tree(self, *args):

        output = {
            self.dp_key: self.secondary_tree["long_name"]
        }

        self.app.vizrt.send_now(output)
