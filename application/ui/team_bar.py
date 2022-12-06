from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
import kivy.properties as kp

class HorizontalTeamBar(Widget):

    teamID = kp.NumericProperty()
    percent = kp.NumericProperty(1)

    def on_percent(self, *args):
        self.resize_bar()

    def on_teamID(self, *args):
        self.resize_bar()

    def on_size(self, *args):
        self.resize_bar()


    def resize_bar(self, *args):

        self.canvas.before.clear()
        
        with self.canvas.before:

            if self.teamID == 100:
                Color(0.31, 0.54, 0.73, 1.0)
            elif self.teamID == 200:
                Color(0.67, 0.26, 0.28, 1.0)
            else:
                Color(1.0, 1.0, 1.0, 1.0)
            
            Rectangle(
                pos=self.pos, 
                size=((self.size[0] * self.percent), self.size[1])
            )


class RightHorizontalTeamBar(HorizontalTeamBar):

    def resize_bar(self, *args):

        self.canvas.before.clear()
        
        with self.canvas.before:

            if self.teamID == 100:
                Color(0.31, 0.54, 0.73, 1.0)
            elif self.teamID == 200:
                Color(0.67, 0.26, 0.28, 1.0)
            else:
                Color(1.0, 1.0, 1.0, 1.0)
            
            Rectangle(
                pos = ((self.pos[0] + self.size[0]), self.pos[1]),
                size = (-(self.size[0] * self.percent), self.size[1])
            )
