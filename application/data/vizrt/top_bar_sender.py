from datetime import datetime

import kivy.properties as kp

from data.events.data_event_dispatch import DataEventDispatcher
from data.vizrt.viz_helper import get_dragon_code

from data.esports.stats import GOLD_DIFF_THRESHOLD
from data.esports.stats import format_signed_number

ADVANTAGE = {
    "even": 0,
    "left": 1,
    "right": 2
}

class TopBarVizSender(DataEventDispatcher):

    # Input Properties
    active = kp.BooleanProperty()
    visible = kp.BooleanProperty()
    clock = kp.StringProperty()

    tricode_left = kp.StringProperty()
    tricode_right = kp.StringProperty()

    viz_logo_left = kp.StringProperty()
    viz_logo_right = kp.StringProperty()

    dragon_left_1 = kp.StringProperty()
    dragon_left_2 = kp.StringProperty()
    dragon_left_3 = kp.StringProperty()
    dragon_left_4 = kp.StringProperty()

    dragon_right_1 = kp.StringProperty()
    dragon_right_2 = kp.StringProperty()
    dragon_right_3 = kp.StringProperty()
    dragon_right_4 = kp.StringProperty()

    gold_left = kp.StringProperty()
    gold_diff_active_left = kp.BooleanProperty(False)
    gold_diff_left = kp.NumericProperty()

    gold_right = kp.StringProperty()
    gold_diff_active_right = kp.BooleanProperty(False)
    gold_diff_right = kp.NumericProperty()

    kills_left = kp.StringProperty()
    kills_right = kp.StringProperty()

    win_record_selector = kp.NumericProperty(0)

    record_left = kp.StringProperty()
    record_right = kp.StringProperty()

    wins_left = kp.StringProperty()
    wins_right = kp.StringProperty()

    towers_left = kp.StringProperty()
    towers_right = kp.StringProperty()

    towers_left_mutator = kp.NumericProperty(0)
    towers_right_mutator = kp.NumericProperty(0)

    #Additional Properties

    dragon_kills_left = kp.NumericProperty(0)
    dragon_kills_right = kp.NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.vizrt.setter('input_data'))

        self.app.config.add_callback(
            self.check_win_or_record,
            section = "User Game Data",
            key="win_or_record"
        )

        self.active = self.app.top_bar.active
        self.app.top_bar.bind(active=self.setter('active'))

        self.visible = self.app.top_bar.visible
        self.app.top_bar.bind(visible=self.setter('visible'))

        self.clock = self.app.top_bar.clock
        self.app.top_bar.bind(clock=self.setter('clock'))

        self.tricode_left = self.app.game_data.tricode_left
        self.app.game_data.bind(tricode_left=self.setter('tricode_left'))
        
        self.tricode_right = self.app.game_data.tricode_right
        self.app.game_data.bind(tricode_right=self.setter('tricode_right'))


        self.viz_logo_left = self.app.viz_mutator.viz_logo_left
        self.app.viz_mutator.bind(viz_logo_left=self.setter('viz_logo_left'))

        self.viz_logo_right = self.app.viz_mutator.viz_logo_right
        self.app.viz_mutator.bind(viz_logo_right=self.setter('viz_logo_right'))


        self.app.top_bar.bind(dragon_left_1=self.setter('dragon_left_1'))
        self.app.top_bar.bind(dragon_left_2=self.setter('dragon_left_2'))
        self.app.top_bar.bind(dragon_left_3=self.setter('dragon_left_3'))
        self.app.top_bar.bind(dragon_left_4=self.setter('dragon_left_4'))

        self.app.top_bar.bind(dragon_right_1=self.setter('dragon_right_1'))
        self.app.top_bar.bind(dragon_right_2=self.setter('dragon_right_2'))
        self.app.top_bar.bind(dragon_right_3=self.setter('dragon_right_3'))
        self.app.top_bar.bind(dragon_right_4=self.setter('dragon_right_4'))

        self.app.top_bar.bind(dragon_kills_left=self.setter('dragon_kills_left'))
        self.app.top_bar.bind(dragon_kills_right=self.setter('dragon_kills_right'))

        self.app.top_bar.bind(gold_left=self.setter('gold_left'))
        self.app.top_bar.bind(gold_diff_left=self.setter('gold_diff_left'))

        self.app.top_bar.bind(gold_right=self.setter('gold_right'))
        self.app.top_bar.bind(gold_diff_right=self.setter('gold_diff_right'))

        self.app.top_bar.bind(kills_left=self.setter('kills_left'))
        self.app.top_bar.bind(kills_right=self.setter('kills_right'))

        self.record_left = self.app.top_bar.record_left
        self.record_right = self.app.top_bar.record_right
        self.app.top_bar.bind(record_left=self.setter('record_left'))
        self.app.top_bar.bind(record_right=self.setter('record_right'))

        self.wins_left = self.app.top_bar.wins_left
        self.wins_right = self.app.top_bar.wins_right
        self.app.top_bar.bind(wins_left=self.setter('wins_left'))
        self.app.top_bar.bind(wins_right=self.setter('wins_right'))

        self.app.top_bar.bind(towers_left=self.setter('towers_left'))
        self.app.top_bar.bind(towers_right=self.setter('towers_right'))

        self.app.top_bar.bind(towers_left_mutator=self.setter('towers_left_mutator'))
        self.app.top_bar.bind(towers_right_mutator=self.setter('towers_right_mutator'))

        self.left_logo_suffix = ""
        self.right_logo_suffix = ""

        self.check_win_or_record()
        

    def on_game_reset(self, *args):

        output = {
            "RESET": str(datetime.now()),
            "ov/active": self.active,
            "ov/show": int(bool(self.visible)),
            "ov/clock": self.clock,
            "ov/dragonsKilledL": self.dragon_kills_left,
            "ov/dragon1L": get_dragon_code(self.dragon_left_1),
            "ov/dragon2L": get_dragon_code(self.dragon_left_2),
            "ov/dragon3L": get_dragon_code(self.dragon_left_3),
            "ov/dragon4L": get_dragon_code(self.dragon_left_4),
            "ov/dragonsKilledR": self.dragon_kills_right,
            "ov/dragon1R": get_dragon_code(self.dragon_right_1),
            "ov/dragon2R": get_dragon_code(self.dragon_right_2),
            "ov/dragon3R": get_dragon_code(self.dragon_right_3),
            "ov/dragon4R": get_dragon_code(self.dragon_right_4),
            "ov/goldL": self.gold_left,
            "ov/goldDiffL":  0,
            "ov/goldDiffActiveL":  int(self.gold_diff_active_left),
            "ov/goldR": self.gold_right,
            "ov/goldDiffR": 0,
            "ov/goldDiffActiveR": int(self.gold_diff_active_right),
            "ov/killsL": self.kills_left,
            "ov/killsR": self.kills_right,
            "ov/recordL": self.record_left,
            "ov/recordR": self.record_right,
            "ov/towersL": f"{(int(self.towers_left) + self.towers_left_mutator)}",
            "ov/towersR": f"{(int(self.towers_right) + self.towers_right_mutator)}",
            "ov/triBlue": "",
            "ov/triBlueLogo": "_Placeholder",
            "ov/triRed": "",
            "ov/triRedLogo": "_Placeholder",
            "ov/winsL": self.wins_left,
            "ov/winsR": self.wins_right,
            "ov/sel": self.win_record_selector
        }

        self.app.vizrt.send_now(output)


    def on_active(self, *args):

        output = {
            "ov/active": self.active
        }

        self.send_data(**output)


    def on_visible(self, *args):

        output = {
            "ov/show": int(bool(self.visible))
        }

        self.send_data(**output)


    def on_clock(self, *args):

        output = {
            "ov/clock": self.clock
        }

        self.send_data(**output)


    def on_dragon_kills_left(self, *args):

        output = {
            "ov/dragonsKilledL": self.dragon_kills_left,
            "ov/dragon1L": get_dragon_code(self.dragon_left_1, 0),
            "ov/dragon2L": get_dragon_code(self.dragon_left_2, 0),
            "ov/dragon3L": get_dragon_code(self.dragon_left_3, 0),
            "ov/dragon4L": get_dragon_code(self.dragon_left_4, 0)
        }

        self.send_data(**output)

    
    def on_dragon_kills_right(self, *args):

        output = {
            "ov/dragonsKilledR": self.dragon_kills_right,
            "ov/dragon1R": get_dragon_code(self.dragon_right_1, 0),
            "ov/dragon2R": get_dragon_code(self.dragon_right_2, 0),
            "ov/dragon3R": get_dragon_code(self.dragon_right_3, 0),
            "ov/dragon4R": get_dragon_code(self.dragon_right_4, 0),
        }

        self.send_data(**output)


    def on_gold_left(self, *args):

        output = {
            "ov/goldL": self.gold_left
        }

        self.send_data(**output)


    def on_gold_diff_left(self, *args):

        new_gold_diff_str = " "

        if self.gold_diff_left > 0:
            new_gold_diff_str = format_signed_number(self.gold_diff_left)


        if self.gold_diff_active_left:
            if self.gold_diff_left <= 0:
                self.gold_diff_active_left = False

        else:
            if self.gold_diff_left >= GOLD_DIFF_THRESHOLD:
                self.gold_diff_active_left = True


        output = {
            "ov/goldDiffL":  new_gold_diff_str,
            "ov/goldDiffActiveL":  int(self.gold_diff_active_left)
        }

        self.send_data(**output)


    def on_gold_right(self, *args):

        output = {
            "ov/goldR": self.gold_right
        }

        self.send_data(**output)


    def on_gold_diff_right(self, *args):

        new_gold_diff_str = " "

        if self.gold_diff_right > 0:
            new_gold_diff_str = format_signed_number(self.gold_diff_right)


        if self.gold_diff_active_right:
            if self.gold_diff_right <= 0:
                self.gold_diff_active_right = False

        else:
            if self.gold_diff_right >= GOLD_DIFF_THRESHOLD:
                self.gold_diff_active_right = True


        output = {
            "ov/goldDiffR":  new_gold_diff_str,
            "ov/goldDiffActiveR":  int(self.gold_diff_active_right)
        }

        self.send_data(**output)


    def on_kills_left(self, *args):

        output = {
            "ov/killsL": self.kills_left
        }

        self.send_data(**output)


    def on_kills_right(self, *args):

        output = {
            "ov/killsR": self.kills_right
        }

        self.send_data(**output)


    def on_towers_left(self, *args):

        output = {
            "ov/towersL": f"{(int(self.towers_left) + self.towers_left_mutator)}",
        }

        self.send_data(**output)

    def on_towers_left_mutator(self, *args):

        output = {
            "ov/towersL": f"{(int(self.towers_left) + self.towers_left_mutator)}"
        }

        self.send_data(**output)


    def on_towers_right(self, *args):

        output = {
            "ov/towersR": f"{(int(self.towers_right) + self.towers_right_mutator)}"
        }

        self.send_data(**output)


    def on_towers_right_mutator(self, *args):

        output = {
            "ov/towersR": f"{(int(self.towers_right) + self.towers_right_mutator)}",
        }

        self.send_data(**output)


    def on_tricode_left(self, *args):
        
        output = {
            "ov/triBlue": self.tricode_left,
            "ov/triBlueLogo": self.viz_logo_left
        }

        self.send_data(**output)


    def on_tricode_right(self, *args):
        
        output = {
            "ov/triRed": self.tricode_right,
            "ov/triRedLogo": self.viz_logo_right
        }

        self.send_data(**output)


    def on_viz_logo_left(self, *args):
        self.on_tricode_left()


    def on_viz_logo_right(self, *args):
        self.on_tricode_right()


    def on_record_left(self, *args):

        output = {
            "ov/recordBlue": self.record_left,
            "ov/sel": self.win_record_selector
        }

        self.send_data(**output)        


    def on_record_right(self, *args):

        output = {
            "ov/recordRed": self.record_right,
            "ov/sel": self.win_record_selector
        }

        self.send_data(**output)


    def on_wins_left(self, *args):

        output = {
            "ov/winsL": self.wins_left,
            "ov/sel": self.win_record_selector
        }

        self.send_data(**output)        


    def on_wins_right(self, *args):

        output = {
            "ov/winsR": self.wins_right,
            "ov/sel": self.win_record_selector
        }

        self.send_data(**output)


    def check_win_or_record(self, *args):

        win_or_record = self.app.config.get(
            "User Game Data",
            "win_or_record",
        )

        result = 0

        if win_or_record == "Record":
            result = 1
        elif win_or_record == "Wins":
            result = 2

        self.win_record_selector = result

        output = {
            "ov/sel": result
        }

        self.send_data(**output)
