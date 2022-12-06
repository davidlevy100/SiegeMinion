import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher

THIS_TEMPLATE_ID = 3
DEFAULT_CHAMP = "_Placeholder"
DEFAULT_LOGO = "_Placeholder"

class DamageBarChartL3VizSender(DataEventDispatcher):

    #Input Properties
    active = kp.BooleanProperty()
    active_title = kp.StringProperty()

    source = kp.ObjectProperty()

    tricode_left = kp.StringProperty()
    tricode_right = kp.StringProperty()

    champ_1 = kp.StringProperty()
    champ_2 = kp.StringProperty()
    champ_3 = kp.StringProperty()
    champ_4 = kp.StringProperty()
    champ_5 = kp.StringProperty()
    champ_6 = kp.StringProperty()
    champ_7 = kp.StringProperty()
    champ_8 = kp.StringProperty()
    champ_9 = kp.StringProperty()
    champ_10 = kp.StringProperty()

    value_1 = kp.StringProperty("")
    value_2 = kp.StringProperty("")
    value_3 = kp.StringProperty("")
    value_4 = kp.StringProperty("")
    value_5 = kp.StringProperty("")
    value_6 = kp.StringProperty("")
    value_7 = kp.StringProperty("")
    value_8 = kp.StringProperty("")
    value_9 = kp.StringProperty("")
    value_10 = kp.StringProperty("")

    percent_1 = kp.NumericProperty(0)
    percent_2 = kp.NumericProperty(0)
    percent_3 = kp.NumericProperty(0)
    percent_4 = kp.NumericProperty(0)
    percent_5 = kp.NumericProperty(0)
    percent_6 = kp.NumericProperty(0)
    percent_7 = kp.NumericProperty(0)
    percent_8 = kp.NumericProperty(0)
    percent_9 = kp.NumericProperty(0)
    percent_10 = kp.NumericProperty(0)
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.game_data.bind(tricode_left=self.setter('tricode_left'))
        self.app.game_data.bind(tricode_right=self.setter('tricode_right'))

        self.bind(output=self.app.vizrt.setter('input_data'))


    def on_source(self, *args):

        self.active = self.source.active
        self.source.bind(active=self.setter('active'))

        self.active_title = self.source.active_title
        self.source.bind(active_title=self.setter('active_title'))

        self.source.bind(champ_1=self.setter('champ_1'))
        self.source.bind(champ_2=self.setter('champ_2'))
        self.source.bind(champ_3=self.setter('champ_3'))
        self.source.bind(champ_4=self.setter('champ_4'))
        self.source.bind(champ_5=self.setter('champ_5'))
        self.source.bind(champ_6=self.setter('champ_6'))
        self.source.bind(champ_7=self.setter('champ_7'))
        self.source.bind(champ_8=self.setter('champ_8'))
        self.source.bind(champ_9=self.setter('champ_9'))
        self.source.bind(champ_10=self.setter('champ_10'))

        self.source.bind(value_1=self.setter('value_1'))
        self.source.bind(value_2=self.setter('value_2'))
        self.source.bind(value_3=self.setter('value_3'))
        self.source.bind(value_4=self.setter('value_4'))
        self.source.bind(value_5=self.setter('value_5'))
        self.source.bind(value_6=self.setter('value_6'))
        self.source.bind(value_7=self.setter('value_7'))
        self.source.bind(value_8=self.setter('value_8'))
        self.source.bind(value_9=self.setter('value_9'))
        self.source.bind(value_10=self.setter('value_10'))

        self.source.bind(percent_1=self.setter('percent_1'))
        self.source.bind(percent_2=self.setter('percent_2'))
        self.source.bind(percent_3=self.setter('percent_3'))
        self.source.bind(percent_4=self.setter('percent_4'))
        self.source.bind(percent_5=self.setter('percent_5'))
        self.source.bind(percent_6=self.setter('percent_6'))
        self.source.bind(percent_7=self.setter('percent_7'))
        self.source.bind(percent_8=self.setter('percent_8'))
        self.source.bind(percent_9=self.setter('percent_9'))
        self.source.bind(percent_10=self.setter('percent_10'))


    def on_game_reset(self, *args):

        output = {
            "l3/templateb": 0,
            "l3/titleb": "",
            "l3/logo1b": DEFAULT_LOGO,
            "l3/logo2b": DEFAULT_LOGO,
            "l3/dmg1": f'\"\"{self.value_1}\"\"',
            "l3/dmg2": f'\"\"{self.value_2}\"\"',
            "l3/dmg3": f'\"\"{self.value_3}\"\"',
            "l3/dmg4": f'\"\"{self.value_4}\"\"',
            "l3/dmg5": f'\"\"{self.value_5}\"\"',
            "l3/dmg6": f'\"\"{self.value_6}\"\"',
            "l3/dmg7": f'\"\"{self.value_7}\"\"',
            "l3/dmg8": f'\"\"{self.value_8}\"\"',
            "l3/dmg9": f'\"\"{self.value_9}\"\"',
            "l3/dmg10": f'\"\"{self.value_10}\"\"',
            "l3/dmgBarWidth1": self.percent_1,
            "l3/dmgBarWidth2": self.percent_2,
            "l3/dmgBarWidth3": self.percent_3,
            "l3/dmgBarWidth4": self.percent_4,
            "l3/dmgBarWidth5": self.percent_5,
            "l3/dmgBarWidth6": self.percent_6,
            "l3/dmgBarWidth7": self.percent_7,
            "l3/dmgBarWidth8": self.percent_8,
            "l3/dmgBarWidth9": self.percent_9,
            "l3/dmgBarWidth10": self.percent_10,
            "l3/champ1": self.get_champ(self.champ_1),
            "l3/champ2": self.get_champ(self.champ_2),
            "l3/champ3": self.get_champ(self.champ_3),
            "l3/champ4": self.get_champ(self.champ_4),
            "l3/champ5": self.get_champ(self.champ_5),
            "l3/champ6": self.get_champ(self.champ_6),
            "l3/champ7": self.get_champ(self.champ_7),
            "l3/champ8": self.get_champ(self.champ_8),
            "l3/champ9": self.get_champ(self.champ_9),
            "l3/champ10": self.get_champ(self.champ_10)
        }

        self.app.vizrt.send_now(output)


    def on_active(self, *args):

        if self.active:
            output = {
                "l3/templateb": THIS_TEMPLATE_ID,
                "l3/titleb": self.active_title,
                "l3/logo1b": self.tricode_left,
                "l3/logo2b": self.tricode_right,
                "l3/dmg1": f'\"\"{self.value_1}\"\"',
                "l3/dmg2": f'\"\"{self.value_2}\"\"',
                "l3/dmg3": f'\"\"{self.value_3}\"\"',
                "l3/dmg4": f'\"\"{self.value_4}\"\"',
                "l3/dmg5": f'\"\"{self.value_5}\"\"',
                "l3/dmg6": f'\"\"{self.value_6}\"\"',
                "l3/dmg7": f'\"\"{self.value_7}\"\"',
                "l3/dmg8": f'\"\"{self.value_8}\"\"',
                "l3/dmg9": f'\"\"{self.value_9}\"\"',
                "l3/dmg10": f'\"\"{self.value_10}\"\"',
                "l3/dmgBarWidth1": self.percent_1,
                "l3/dmgBarWidth2": self.percent_2,
                "l3/dmgBarWidth3": self.percent_3,
                "l3/dmgBarWidth4": self.percent_4,
                "l3/dmgBarWidth5": self.percent_5,
                "l3/dmgBarWidth6": self.percent_6,
                "l3/dmgBarWidth7": self.percent_7,
                "l3/dmgBarWidth8": self.percent_8,
                "l3/dmgBarWidth9": self.percent_9,
                "l3/dmgBarWidth10": self.percent_10,
                "l3/champ1": self.get_champ(self.champ_1),
                "l3/champ2": self.get_champ(self.champ_2),
                "l3/champ3": self.get_champ(self.champ_3),
                "l3/champ4": self.get_champ(self.champ_4),
                "l3/champ5": self.get_champ(self.champ_5),
                "l3/champ6": self.get_champ(self.champ_6),
                "l3/champ7": self.get_champ(self.champ_7),
                "l3/champ8": self.get_champ(self.champ_8),
                "l3/champ9": self.get_champ(self.champ_9),
                "l3/champ10": self.get_champ(self.champ_10)
            }

            self.send_data(**output)


    def get_champ(self, champ, *args):

        if (champ == "" or 
            champ == "default"
        ):
            return DEFAULT_CHAMP

        else:
            return champ