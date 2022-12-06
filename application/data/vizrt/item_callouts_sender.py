import kivy.properties as kp

from data.events.data_event_dispatch import DataEventDispatcher

class ItemCalloutsVizSender(DataEventDispatcher):

    tricode_left = kp.StringProperty("BLUE")
    tricode_right = kp.StringProperty("RED")

    player1_callout_item = kp.DictProperty(allownone=True)
    player2_callout_item = kp.DictProperty(allownone=True)
    player3_callout_item = kp.DictProperty(allownone=True)
    player4_callout_item = kp.DictProperty(allownone=True)
    player6_callout_item = kp.DictProperty(allownone=True)
    player5_callout_item = kp.DictProperty(allownone=True)
    player6_callout_item = kp.DictProperty(allownone=True)
    player7_callout_item = kp.DictProperty(allownone=True)
    player8_callout_item = kp.DictProperty(allownone=True)
    player9_callout_item = kp.DictProperty(allownone=True)
    player10_callout_item = kp.DictProperty(allownone=True)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.game_data.bind(tricode_left=self.setter('tricode_left'))
        self.app.game_data.bind(tricode_right=self.setter('tricode_right'))

        self.app.overlay_players.player1.inventory.bind(callout_item=self.setter('player1_callout_item'))
        self.app.overlay_players.player2.inventory.bind(callout_item=self.setter('player2_callout_item'))
        self.app.overlay_players.player3.inventory.bind(callout_item=self.setter('player3_callout_item'))
        self.app.overlay_players.player4.inventory.bind(callout_item=self.setter('player4_callout_item'))
        self.app.overlay_players.player5.inventory.bind(callout_item=self.setter('player5_callout_item'))

        self.app.overlay_players.player6.inventory.bind(callout_item=self.setter('player6_callout_item'))
        self.app.overlay_players.player7.inventory.bind(callout_item=self.setter('player7_callout_item'))
        self.app.overlay_players.player8.inventory.bind(callout_item=self.setter('player8_callout_item'))
        self.app.overlay_players.player9.inventory.bind(callout_item=self.setter('player9_callout_item'))
        self.app.overlay_players.player10.inventory.bind(callout_item=self.setter('player10_callout_item'))

        self.bind(output=self.app.vizrt.setter('input_data'))

        self.default_item = self.app.data_dragon.get_asset(
            "item",
            "default"
        )

    def on_player1_callout_item(self, *args):

        if args[1] is not None:

            item = args[1]

            self.send_item("L1", True, self.tricode_left, item)

        else:
            self.send_item("L1", False, "", self.default_item)


    def on_player2_callout_item(self, *args):

        if args[1] is not None:

            item = args[1]

            self.send_item("L2", True, self.tricode_left, item)

        else:
            self.send_item("L2", False, "", self.default_item)


    def on_player3_callout_item(self, *args):

        if args[1] is not None:

            item = args[1]

            self.send_item("L3", True, self.tricode_left, item)

        else:
            self.send_item("L3", False, "", self.default_item)


    def on_player4_callout_item(self, *args):

        if args[1] is not None:

            item = args[1]

            self.send_item("L4", True, self.tricode_left, item)

        else:
            self.send_item("L4", False, "", self.default_item)


    def on_player5_callout_item(self, *args):

        if args[1] is not None:

            item = args[1]

            self.send_item("L5", True, self.tricode_left, item)

        else:
            self.send_item("L5", False, "", self.default_item)


    def on_player6_callout_item(self, *args):

        if args[1] is not None:

            item = args[1]

            self.send_item("R1", True, self.tricode_right, item)

        else:
            self.send_item("R1", False, "", self.default_item)


    def on_player7_callout_item(self, *args):

        if args[1] is not None:

            item = args[1]

            self.send_item("R2", True, self.tricode_right, item)

        else:
            self.send_item("R2", False, "", self.default_item)


    def on_player8_callout_item(self, *args):

        if args[1] is not None:

            item = args[1]

            self.send_item("R3", True, self.tricode_right, item)

        else:
            self.send_item("R3", False, "", self.default_item)


    def on_player9_callout_item(self, *args):

        if args[1] is not None:

            item = args[1]

            self.send_item("R4", True, self.tricode_right, item)

        else:
            self.send_item("R4", False, "", self.default_item)


    def on_player10_callout_item(self, *args):

        if args[1] is not None:

            item = args[1]

            self.send_item("R5", True, self.tricode_right, item)

        else:
            self.send_item("R5", False, "", self.default_item)

    
    def send_item(self, position, active, tricode, item, *args):

        if ("internal_name" in item and
            "external_name" in item
        ):

            text = item["external_name"]
            image = item["internal_name"]

            output = {
                f"item{position}/anim": int(active),
                f"item{position}/tri": tricode,
                f"item{position}/itemImage": image,
                f"item{position}/itemText": text
            }

            self.output = output
