import kivy.properties as kp
from kivy.logger import Logger

from data.vizrt.vizcrank.sender import VizcrankSender
from data.esports.stats import convert_milliseconds_to_HMS_string


FIELD_PREFIXES = {
    0: 100,
    1: 200,
    2: 300,
    3: 400,
    4: 500, 
    5: 120,
    6: 220,
    7: 320,
    8: 420,
    9: 520
}


class L3PauseGraphicSender(VizcrankSender):

    tricode_left = kp.StringProperty()
    tricode_right = kp.StringProperty()

    viz_logo_left = kp.StringProperty()
    viz_logo_right = kp.StringProperty()

    # TODO need to figure out how to bind to turretdispatcher
    blue_turret_kill_quantity = kp.NumericProperty(0)
    red_turret_kill_quantity = kp.NumericProperty(0)

    pause_started_event = kp.DictProperty({})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.live_data.bind(pause_started_event=self.setter('pause_started_event'))
        self.app.game_data.bind(tricode_left=self.setter('tricode_left'))
        self.app.game_data.bind(tricode_right=self.setter('tricode_right'))

        self.viz_logo_left = self.app.viz_mutator.viz_logo_left
        self.app.viz_mutator.bind(viz_logo_left=self.setter('viz_logo_left'))

        self.viz_logo_right = self.app.viz_mutator.viz_logo_right
        self.app.viz_mutator.bind(viz_logo_right=self.setter('viz_logo_right'))

        #Config Keys
        self.section = "L3 Pause Graphic"

    
    def on_pause_started_event(self, *args):

        if not self.can_process():
            return

        if not (self.auto_slack or self.auto_trio):
            return

        if self.auto_slack:
            self.send_to_slack()

        if self.auto_trio:
            self.send_to_trio()


    def can_process(self, *args):

        if len(self.pause_started_event) == 0:
            return False

        else:
            return True

    def process_game_data(self, game_data, *args):
        # Turn Dots Off
        field = "0001"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = 0

        # Left Team Logo
        field = "0100"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = self.viz_logo_left

        # Right Team Logo
        field = "0200"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = self.viz_logo_right

        # Game Time
        field = "0060"
        # TODO need to look at pause_event to get game time from that

        # Left Towers
        # Need live towers, not historical
        field = "0121"

        # Right Towers
        # Need live towers, not historical
        field = "0221"

        # Left Gold
        field = "0221"

        # Dragon images


        return game_data  
