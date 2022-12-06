from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.logger import Logger
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import kivy.properties as kp

from ui.team_color_grid_layout import TeamColorGridLayout 
from ui.warning_layout import DynamicGridWarningLayout
from ui.icons import ElderImage, DragonImage
from ui.black_label import BlackLabel


from ui.constants.text import SPAWN_TEXT, BUFF_TEXT, TEAM_TEXT


class DragonLayout(GridLayout):

    mode = kp.OptionProperty (
        "next_dragon",
        options=[
            "next_dragon",
            "elder_dragon"
        ]
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()
        self.rows = 1

        self.app.next_dragon.bind(mode=self.setter('mode'))

        self.next_dragon_layout = NextDragonLayout()
        self.elder_dragon_layout = ElderDragonLayout()

        self.on_mode()


    def on_mode(self, *args):
        self.clear_widgets()

        if self.mode == "next_dragon":
            self.add_widget(self.next_dragon_layout)
        elif self.mode == "elder_dragon":
            self.add_widget(self.elder_dragon_layout)


class NextDragonLayout(TeamColorGridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()

        self.rows = 1

        #Column 1, Dragon Image
        self.image_layout = GridLayout(
            rows = 1,
            padding = 5,
            size_hint_x = 0.25
        )

        self.image = DragonImage()
        self.app.next_dragon.bind(next_dragon_name=self.image.setter('dragon_type'))
        self.image_layout.add_widget(self.image)

        self.add_widget(self.image_layout)

        #Column 2, respawn timer
        self.timer_label = Label(text=self.app.next_dragon.respawn_timer_string)
        self.app.next_dragon.bind(respawn_timer_string=self.timer_label.setter('text'))

        self.add_widget(self.timer_label)






class ElderDragonLayout(TeamColorGridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()

        self.rows = 1
        self.app.elder_dragon.bind(teamID=self.setter('teamID'))
        self.padding = 5


        # Elder Image
        self.image_layout = GridLayout(
            rows = 1,
            size_hint_x = 0.5 
        )
        self.image_layout.add_widget(ElderImage())
        self.add_widget(self.image_layout)

        self.data_layout = GridLayout(
            rows = 1
        )

        # Timer
        self.timer_label = Label(text=self.app.elder_dragon.buff_timer_string)
        self.app.elder_dragon.bind(buff_timer_string=self.timer_label.setter('text'))
        
        self.data_layout.add_widget(self.timer_label)
    

        # Respawn Timer

        self.respawn_timer_label = Label(text=self.app.elder_dragon.respawn_timer_string)
        self.app.elder_dragon.bind(respawn_timer_string=self.respawn_timer_label.setter('text'))
        self.data_layout.add_widget(self.respawn_timer_label)


        self.add_widget(self.data_layout)
