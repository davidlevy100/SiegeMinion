import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher
from data.vizrt.viz_helper import sanitize_number, two_line

THIS_TEMPLATE_ID = 2
DEFAULT_CHAMP = "_Placeholder"
DEFAULT_LOGO = "_Placeholder"
DEFAULT_PLAYER = "_Placeholder"

class PlayerMatchupL3VizSender(DataEventDispatcher):

    #Input Properties
    active = kp.BooleanProperty()
    active_title = kp.StringProperty()

    source = kp.ObjectProperty()

    tricode_left = kp.StringProperty()
    tricode_right = kp.StringProperty()

    active_left_player_name = kp.StringProperty("")
    active_right_player_name = kp.StringProperty("")

    active_left_champion = kp.DictProperty()
    active_right_champion = kp.DictProperty()

    active_cat1 = kp.StringProperty("")
    active_cat2 = kp.StringProperty("")
    active_cat3 = kp.StringProperty("")
    active_cat4 = kp.StringProperty("")

    active_left_stat1 = kp.StringProperty("")
    active_left_stat2 = kp.StringProperty("")
    active_left_stat3 = kp.StringProperty("")
    active_left_stat4 = kp.StringProperty("")

    active_right_stat1 = kp.StringProperty("")
    active_right_stat2 = kp.StringProperty("")
    active_right_stat3 = kp.StringProperty("")
    active_right_stat4 = kp.StringProperty("")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.game_data.bind(tricode_left=self.setter('tricode_left'))
        self.app.game_data.bind(tricode_right=self.setter('tricode_right'))

        self.bind(output=self.app.vizrt.setter('input_data'))


    def on_active(self, *args):

        if self.active:
            output = {
                "l3/templateb": THIS_TEMPLATE_ID,
                "l3/titleb": self.active_title,
                "l3/logo1b": self.tricode_left,
                "l3/logo2b": self.tricode_right,
                "l3/player1b": self.active_left_player_name.upper(),
                "l3/playerImage1b": f"{self.tricode_left}/{self.active_left_player_name.upper()}",
                "l3/player2b": self.active_right_player_name.upper(),
                "l3/playerImage2b": f"{self.tricode_right}/{self.active_right_player_name.upper()}",
                "l3/champIcon1b": self.get_champ(self.active_left_champion),
                "l3/champIcon2b": self.get_champ(self.active_right_champion),
                "l3/cat1b": self.active_cat1,
                "l3/cat2b": self.active_cat2,
                "l3/cat3b": self.active_cat3,
                "l3/cat4b": self.active_cat4,
                "l3/stat1Ab": two_line(sanitize_number(self.active_left_stat1)),
                "l3/stat1Bb": two_line(sanitize_number(self.active_right_stat1)),
                "l3/stat2Ab": two_line(sanitize_number(self.active_left_stat2)),
                "l3/stat2Bb": two_line(sanitize_number(self.active_right_stat2)),
                "l3/stat3Ab": two_line(sanitize_number(self.active_left_stat3)),
                "l3/stat3Bb": two_line(sanitize_number(self.active_right_stat3)),
                "l3/stat4Ab": two_line(sanitize_number(self.active_left_stat4)),
                "l3/stat4Bb": two_line(sanitize_number(self.active_right_stat4))
            }

            self.send_data(**output)


    def on_active_left_stat1(self, *args):

        output = {
            "l3/stat1Ab": two_line(sanitize_number(self.active_left_stat1))
        }

        self.send_data(**output)


    def on_active_left_stat2(self, *args):

        output = {
            "l3/stat2Ab": two_line(sanitize_number(self.active_left_stat2))
        }

        self.send_data(**output)


    def on_active_left_stat3(self, *args):

        output = {
            "l3/stat3Ab": two_line(sanitize_number(self.active_left_stat3))
        }

        self.send_data(**output)


    def on_active_left_stat4(self, *args):

        output = {
            "l3/stat4Ab": two_line(sanitize_number(self.active_left_stat4))
        }

        self.send_data(**output)


    def on_active_right_stat1(self, *args):

        output = {
            "l3/stat1Bb": two_line(sanitize_number(self.active_right_stat1))
        }

        self.send_data(**output)


    def on_active_right_stat2(self, *args):

        output = {
            "l3/stat2Bb": two_line(sanitize_number(self.active_right_stat2))
        }

        self.send_data(**output)


    def on_active_right_stat3(self, *args):

        output = {
            "l3/stat3Bb": two_line(sanitize_number(self.active_right_stat3))
        }

        self.send_data(**output)

    
    def on_active_right_stat4(self, *args):

        output = {
            "l3/stat4Bb": two_line(sanitize_number(self.active_right_stat4))
        }

        self.send_data(**output)


    def on_source(self, *args):

        self.active = self.source.active
        self.source.bind(active=self.setter('active'))

        self.active_title = self.source.active_title
        self.source.bind(active_title=self.setter('active_title'))

        self.source.bind(active_left_player_name=self.setter('active_left_player_name'))
        self.source.bind(active_right_player_name=self.setter('active_right_player_name'))

        self.source.bind(active_left_champion=self.setter('active_left_champion'))
        self.source.bind(active_right_champion=self.setter('active_right_champion'))

        self.source.bind(active_cat1=self.setter('active_cat1'))
        self.source.bind(active_cat2=self.setter('active_cat2'))
        self.source.bind(active_cat3=self.setter('active_cat3'))
        self.source.bind(active_cat4=self.setter('active_cat4'))

        self.source.bind(active_left_stat1=self.setter('active_left_stat1'))
        self.source.bind(active_left_stat2=self.setter('active_left_stat2'))
        self.source.bind(active_left_stat3=self.setter('active_left_stat3'))
        self.source.bind(active_left_stat4=self.setter('active_left_stat4'))

        self.source.bind(active_right_stat1=self.setter('active_right_stat1'))
        self.source.bind(active_right_stat2=self.setter('active_right_stat2'))
        self.source.bind(active_right_stat3=self.setter('active_right_stat3'))
        self.source.bind(active_right_stat4=self.setter('active_right_stat4'))


    def get_champ(self, champ, *args):

        champ_name = DEFAULT_CHAMP

        if "internal_name" in champ:
            champ_name = champ["internal_name"]

        return champ_name

