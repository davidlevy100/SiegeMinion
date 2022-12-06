import kivy.properties as kp

from data.events.data_event_dispatch import DataEventDispatcher

CALLOUT_LEVELS = [6,11,16,18]

class LevelCalloutsVizSender(DataEventDispatcher):

    player1_level = kp.NumericProperty(0)
    player2_level = kp.NumericProperty(0)
    player3_level = kp.NumericProperty(0)
    player4_level = kp.NumericProperty(0)
    player5_level = kp.NumericProperty(0)
    player6_level = kp.NumericProperty(0)
    player7_level = kp.NumericProperty(0)
    player8_level = kp.NumericProperty(0)
    player9_level = kp.NumericProperty(0)
    player10_level = kp.NumericProperty(0)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.vizrt.setter('input_data'))

        self.app.overlay_players.player1.bind(level=self.setter('player1_level'))
        self.app.overlay_players.player2.bind(level=self.setter('player2_level'))
        self.app.overlay_players.player3.bind(level=self.setter('player3_level'))
        self.app.overlay_players.player4.bind(level=self.setter('player4_level'))
        self.app.overlay_players.player5.bind(level=self.setter('player5_level'))
        self.app.overlay_players.player6.bind(level=self.setter('player6_level'))
        self.app.overlay_players.player7.bind(level=self.setter('player7_level'))
        self.app.overlay_players.player8.bind(level=self.setter('player8_level'))
        self.app.overlay_players.player9.bind(level=self.setter('player9_level'))
        self.app.overlay_players.player10.bind(level=self.setter('player10_level'))


    def on_player1_level(self, *args):

        if args[1] in CALLOUT_LEVELS:

            self.send_level("L1", True, args[1])

        else:
            self.send_level("L1", False, args[1])


    def on_player2_level(self, *args):

        if args[1] in CALLOUT_LEVELS:

            self.send_level("L2", True, args[1])

        else:
            self.send_level("L2", False, args[1])


    def on_player3_level(self, *args):

        if args[1] in CALLOUT_LEVELS:

            self.send_level("L3", True, args[1])

        else:
            self.send_level("L3", False, args[1])


    def on_player4_level(self, *args):

        if args[1] in CALLOUT_LEVELS:

            self.send_level("L4", True, args[1])

        else:
            self.send_level("L4", False, args[1])


    def on_player5_level(self, *args):

        if args[1] in CALLOUT_LEVELS:

            self.send_level("L5", True, args[1])

        else:
            self.send_level("L5", False, args[1])


    def on_player6_level(self, *args):

        if args[1] in CALLOUT_LEVELS:

            self.send_level("R1", True, args[1])

        else:
            self.send_level("R1", False, args[1])


    def on_player7_level(self, *args):

        if args[1] in CALLOUT_LEVELS:

            self.send_level("R2", True, args[1])

        else:
            self.send_level("R2", False, args[1])


    def on_player8_level(self, *args):

        if args[1] in CALLOUT_LEVELS:

            self.send_level("R3", True, args[1])

        else:
            self.send_level("R3", False, args[1])


    def on_player9_level(self, *args):

        if args[1] in CALLOUT_LEVELS:

            self.send_level("R4", True, args[1])

        else:
            self.send_level("R4", False, args[1])


    def on_player10_level(self, *args):

        if args[1] in CALLOUT_LEVELS:

            self.send_level("R5", True, args[1])

        else:
            self.send_level("R5", False, args[1])


    def send_level(self, position, active, level, *args):

        output = {
            f"level{position}/anim": int(active),
            f"level{position}/levelText": level
        }

        self.output = output
