import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher
from data.vizrt.viz_helper import sanitize_number, two_line

THIS_TEMPLATE_ID = 1
DEFAULT_CHAMP = "_Placeholder"
DEFAULT_RUNE = "_Placeholder"

class PlayerRunesL3VizSender(DataEventDispatcher):

    #Input Properties
    active = kp.BooleanProperty()
    active_title = kp.StringProperty()

    source = kp.ObjectProperty()

    active_player_name = kp.StringProperty("")
    active_tricode = kp.StringProperty("")

    active_champion = kp.DictProperty()

    active_primary_tree = kp.DictProperty(allownone=True)
    active_secondary_tree = kp.DictProperty(allownone=True)

    active_keystone = kp.DictProperty(allownone=True)

    active_rune1 = kp.DictProperty(allownone=True)
    active_rune2 = kp.DictProperty(allownone=True)
    active_rune3 = kp.DictProperty(allownone=True)
    active_rune4 = kp.DictProperty(allownone=True)
    active_rune5 = kp.DictProperty(allownone=True)



    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.vizrt.setter('input_data'))


    def on_active(self, *args):

        if self.active:
            output = {
                "l3/templateb": THIS_TEMPLATE_ID,
                "l3/titleb": self.active_title,
                "l3/logo1b": self.active_tricode,
                "l3/player1b": self.active_player_name.upper(),
                "l3/playerImage1b": f"{self.active_tricode}/{self.active_player_name.upper()}",
                "l3/champIcon1b": self.get_champ(self.active_champion),
                "l3/runeTree1b": self.get_rune(self.active_primary_tree),
                "l3/mainRune1b": self.get_rune(self.active_keystone),
                "l3/subRune1b": self.get_rune(self.active_rune1),
                "l3/subRune2b": self.get_rune(self.active_rune2),
                "l3/subRune3b": self.get_rune(self.active_rune3),
                "l3/runeTree2b": self.get_rune(self.active_secondary_tree),
                "l3/subRune4b": self.get_rune(self.active_rune4),
                "l3/subRune5b": self.get_rune(self.active_rune5)
            }

            self.send_data(**output)


    def on_source(self, *args):

        self.active = self.source.active
        self.source.bind(active=self.setter('active'))

        self.active_title = self.source.active_title
        self.source.bind(active_title=self.setter('active_title'))

        self.source.bind(active_player_name=self.setter('active_player_name'))

        self.source.bind(active_tricode=self.setter('active_tricode'))

        self.source.bind(active_champion=self.setter('active_champion'))

        self.source.bind(active_primary_tree=self.setter('active_primary_tree'))
        self.source.bind(active_secondary_tree=self.setter('active_secondary_tree'))

        self.source.bind(active_keystone=self.setter('active_keystone'))

        self.source.bind(active_rune1=self.setter('active_rune1'))
        self.source.bind(active_rune2=self.setter('active_rune2'))
        self.source.bind(active_rune3=self.setter('active_rune3'))
        self.source.bind(active_rune4=self.setter('active_rune4'))
        self.source.bind(active_rune5=self.setter('active_rune5'))

    
    def get_champ(self, champ, *args):

        champ_name = DEFAULT_CHAMP

        if "internal_name" in champ:
            champ_name = champ["internal_name"]

        return champ_name


    def get_rune(self, rune, *args):

        rune_name = DEFAULT_RUNE

        if "long_name" in rune:
            rune_name = rune["long_name"]

        return rune_name

