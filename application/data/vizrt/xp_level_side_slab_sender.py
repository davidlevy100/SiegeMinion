import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher


DEFAULT_CHAMP = "_Placeholder"

DP_KEY = "xpLevel/xpl"

THIS_TEMPLATE_ID = 3


class XPLevelSideSlabVizSender(DataEventDispatcher):

    # Input Properties
    source = kp.ObjectProperty()

    local_time = kp.NumericProperty()

    active = kp.BooleanProperty(False)
    active_title = kp.StringProperty()

    tricode_left = kp.StringProperty()
    tricode_right = kp.StringProperty()

    bar_teamID_1 = kp.NumericProperty(100)
    bar_teamID_2 = kp.NumericProperty(100)
    bar_teamID_3 = kp.NumericProperty(100)
    bar_teamID_4 = kp.NumericProperty(100)
    bar_teamID_5 = kp.NumericProperty(100)
    bar_teamID_6 = kp.NumericProperty(200)
    bar_teamID_7 = kp.NumericProperty(200)
    bar_teamID_8 = kp.NumericProperty(200)
    bar_teamID_9 = kp.NumericProperty(200)
    bar_teamID_10 = kp.NumericProperty(200)

    champ_1 = kp.StringProperty("")
    champ_2 = kp.StringProperty("")
    champ_3 = kp.StringProperty("")
    champ_4 = kp.StringProperty("")
    champ_5 = kp.StringProperty("")
    champ_6 = kp.StringProperty("")
    champ_7 = kp.StringProperty("")
    champ_8 = kp.StringProperty("")
    champ_9 = kp.StringProperty("")
    champ_10 = kp.StringProperty("")

    player_name_1 = kp.StringProperty("")
    player_name_2 = kp.StringProperty("")
    player_name_3 = kp.StringProperty("")
    player_name_4 = kp.StringProperty("")
    player_name_5 = kp.StringProperty("")
    player_name_6 = kp.StringProperty("")
    player_name_7 = kp.StringProperty("")
    player_name_8 = kp.StringProperty("")
    player_name_9 = kp.StringProperty("")
    player_name_10 = kp.StringProperty("")

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

    level_1 = kp.StringProperty("")
    level_2 = kp.StringProperty("")
    level_3 = kp.StringProperty("")
    level_4 = kp.StringProperty("")
    level_5 = kp.StringProperty("")
    level_6 = kp.StringProperty("")
    level_7 = kp.StringProperty("")
    level_8 = kp.StringProperty("")
    level_9 = kp.StringProperty("")
    level_10 = kp.StringProperty("")

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

        self.app.livestats_history.bind(
            local_time=self.setter('local_time')
        )

        self.app.game_data.bind(tricode_left=self.setter('tricode_left'))
        self.app.game_data.bind(tricode_right=self.setter('tricode_right'))

        self.bind(output=self.app.vizrt.setter('input_data'))

    
    def on_source(self, *args):

        self.active = self.source.active
        self.source.bind(active=self.setter('active'))

        self.active_title = self.source.active_title
        self.source.bind(active_title=self.setter('active_title'))

        self.source.bind(bar_teamID_1=self.setter('bar_teamID_1'))
        self.source.bind(bar_teamID_2=self.setter('bar_teamID_2'))
        self.source.bind(bar_teamID_3=self.setter('bar_teamID_3'))
        self.source.bind(bar_teamID_4=self.setter('bar_teamID_4'))
        self.source.bind(bar_teamID_5=self.setter('bar_teamID_5'))
        self.source.bind(bar_teamID_6=self.setter('bar_teamID_6'))
        self.source.bind(bar_teamID_7=self.setter('bar_teamID_7'))
        self.source.bind(bar_teamID_8=self.setter('bar_teamID_8'))
        self.source.bind(bar_teamID_9=self.setter('bar_teamID_9'))
        self.source.bind(bar_teamID_10=self.setter('bar_teamID_10'))

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

        self.source.bind(player_name_1=self.setter('player_name_1'))
        self.source.bind(player_name_2=self.setter('player_name_2'))
        self.source.bind(player_name_3=self.setter('player_name_3'))
        self.source.bind(player_name_4=self.setter('player_name_4'))
        self.source.bind(player_name_5=self.setter('player_name_5'))
        self.source.bind(player_name_6=self.setter('player_name_6'))
        self.source.bind(player_name_7=self.setter('player_name_7'))
        self.source.bind(player_name_8=self.setter('player_name_8'))
        self.source.bind(player_name_9=self.setter('player_name_9'))
        self.source.bind(player_name_10=self.setter('player_name_10'))

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

        self.source.bind(level_1=self.setter('level_1'))
        self.source.bind(level_2=self.setter('level_2'))
        self.source.bind(level_3=self.setter('level_3'))
        self.source.bind(level_4=self.setter('level_4'))
        self.source.bind(level_5=self.setter('level_5'))
        self.source.bind(level_6=self.setter('level_6'))
        self.source.bind(level_7=self.setter('level_7'))
        self.source.bind(level_8=self.setter('level_8'))
        self.source.bind(level_9=self.setter('level_9'))
        self.source.bind(level_10=self.setter('level_10'))

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


    def on_active(self, *args):

        if self.active:
            self.update_vizrt()

        else:
            output = {
                "ss/anim": int(self.active)
            }

            self.app.vizrt.send_now(output) 


    def on_local_time(self, *args):

        if self.active:
            self.update_vizrt()


    def on_game_reset(self, *args):

        output = self.construct_output(0)        
        self.app.vizrt.send_now(output)

    
    def update_vizrt(self, *args):

        output = self.construct_output(THIS_TEMPLATE_ID)
        self.send_data(**output)


    def construct_output(self, template_id):

        output = {
            "ss/templateb": template_id,
            "ss/titleb": self.active_title,
            "ss/anim": int(self.active),
            f"ss/{DP_KEY}1/barColor": self.get_team_color(self.bar_teamID_1),
            f"ss/{DP_KEY}2/barColor": self.get_team_color(self.bar_teamID_2),
            f"ss/{DP_KEY}3/barColor": self.get_team_color(self.bar_teamID_3),
            f"ss/{DP_KEY}4/barColor": self.get_team_color(self.bar_teamID_4),
            f"ss/{DP_KEY}5/barColor": self.get_team_color(self.bar_teamID_5),
            f"ss/{DP_KEY}6/barColor": self.get_team_color(self.bar_teamID_6),
            f"ss/{DP_KEY}7/barColor": self.get_team_color(self.bar_teamID_7),
            f"ss/{DP_KEY}8/barColor": self.get_team_color(self.bar_teamID_8),
            f"ss/{DP_KEY}9/barColor": self.get_team_color(self.bar_teamID_9),
            f"ss/{DP_KEY}10/barColor": self.get_team_color(self.bar_teamID_10),
            f"ss/{DP_KEY}1/barWidth": self.percent_1,
            f"ss/{DP_KEY}2/barWidth": self.percent_2,
            f"ss/{DP_KEY}3/barWidth": self.percent_3,
            f"ss/{DP_KEY}4/barWidth": self.percent_4,
            f"ss/{DP_KEY}5/barWidth": self.percent_5,
            f"ss/{DP_KEY}6/barWidth": self.percent_6,
            f"ss/{DP_KEY}7/barWidth": self.percent_7,
            f"ss/{DP_KEY}8/barWidth": self.percent_8,
            f"ss/{DP_KEY}9/barWidth": self.percent_9,
            f"ss/{DP_KEY}10/barWidth": self.percent_10,
            f"ss/{DP_KEY}1/champIcon": self.get_champ(self.champ_1),
            f"ss/{DP_KEY}2/champIcon": self.get_champ(self.champ_2),
            f"ss/{DP_KEY}3/champIcon": self.get_champ(self.champ_3),
            f"ss/{DP_KEY}4/champIcon": self.get_champ(self.champ_4),
            f"ss/{DP_KEY}5/champIcon": self.get_champ(self.champ_5),
            f"ss/{DP_KEY}6/champIcon": self.get_champ(self.champ_6),
            f"ss/{DP_KEY}7/champIcon": self.get_champ(self.champ_7),
            f"ss/{DP_KEY}8/champIcon": self.get_champ(self.champ_8),
            f"ss/{DP_KEY}9/champIcon": self.get_champ(self.champ_9),
            f"ss/{DP_KEY}10/champIcon": self.get_champ(self.champ_10),
            f"ss/{DP_KEY}1/playerName": self.player_name_1,
            f"ss/{DP_KEY}2/playerName": self.player_name_2,
            f"ss/{DP_KEY}3/playerName": self.player_name_3,
            f"ss/{DP_KEY}4/playerName": self.player_name_4,
            f"ss/{DP_KEY}5/playerName": self.player_name_5,
            f"ss/{DP_KEY}6/playerName": self.player_name_6,
            f"ss/{DP_KEY}7/playerName": self.player_name_7,
            f"ss/{DP_KEY}8/playerName": self.player_name_8,
            f"ss/{DP_KEY}9/playerName": self.player_name_9,
            f"ss/{DP_KEY}10/playerName": self.player_name_10,
            f"ss/{DP_KEY}1/value": f'\"\"{self.value_1}\"\"',
            f"ss/{DP_KEY}2/value": f'\"\"{self.value_2}\"\"',
            f"ss/{DP_KEY}3/value": f'\"\"{self.value_3}\"\"',
            f"ss/{DP_KEY}4/value": f'\"\"{self.value_4}\"\"',
            f"ss/{DP_KEY}5/value": f'\"\"{self.value_5}\"\"',
            f"ss/{DP_KEY}6/value": f'\"\"{self.value_6}\"\"',
            f"ss/{DP_KEY}7/value": f'\"\"{self.value_7}\"\"',
            f"ss/{DP_KEY}8/value": f'\"\"{self.value_8}\"\"',
            f"ss/{DP_KEY}9/value": f'\"\"{self.value_9}\"\"',
            f"ss/{DP_KEY}10/value": f'\"\"{self.value_10}\"\"',
            f"ss/{DP_KEY}1/level": f'\"\"{self.level_1}\"\"',
            f"ss/{DP_KEY}2/level": f'\"\"{self.level_2}\"\"',
            f"ss/{DP_KEY}3/level": f'\"\"{self.level_3}\"\"',
            f"ss/{DP_KEY}4/level": f'\"\"{self.level_4}\"\"',
            f"ss/{DP_KEY}5/level": f'\"\"{self.level_5}\"\"',
            f"ss/{DP_KEY}6/level": f'\"\"{self.level_6}\"\"',
            f"ss/{DP_KEY}7/level": f'\"\"{self.level_7}\"\"',
            f"ss/{DP_KEY}8/level": f'\"\"{self.level_8}\"\"',
            f"ss/{DP_KEY}9/level": f'\"\"{self.level_9}\"\"',
            f"ss/{DP_KEY}10/level": f'\"\"{self.level_10}\"\"'
        }

        return output


    def get_team_color(self, teamID):

        if teamID == 100:
            return 0
        
        elif teamID == 200:
            return 1

        else:
            return None

    
    def get_champ(self, champ, *args):

        if (champ == "" or 
            champ == "default"
        ):
            return DEFAULT_CHAMP

        else:
            return champ