from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
import kivy.properties as kp

from ui.constants.colors import BLACK_BG, BLUE_BG, RED_BG

class TeamColorGridLayout(GridLayout):

    teamID = kp.NumericProperty()
    bg_color = kp.ListProperty(BLACK_BG)

    def on_teamID(self, *args):

        if self.teamID == 100:
            self.bg_color = BLUE_BG

        elif self.teamID == 200:
            self.bg_color = RED_BG

        else:
            self.bg_color = BLACK_BG

        self.set_bg_color()


    def on_size(self, *args):
        self.set_bg_color()


    def set_bg_color(self, *args):

        self.canvas.before.clear()
        with self.canvas.before:
            Color(
                self.bg_color[0],
                self.bg_color[1],
                self.bg_color[2],
                self.bg_color[3]
            )
            Rectangle(
                pos=self.pos, 
                size=self.size
            )
