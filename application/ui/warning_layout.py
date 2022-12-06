from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
import kivy.properties as kp

from ui.constants.colors import STATUS_COLORS, STATUS_OPTIONS


class GridWarningLayout(GridLayout):

    status = kp.OptionProperty(STATUS_OPTIONS[0], options=STATUS_OPTIONS)
    status_color = kp.ListProperty(STATUS_COLORS[STATUS_OPTIONS[0]])

    def on_status(self, *args):    
        self.status_color = STATUS_COLORS[self.status]


class DynamicGridWarningLayout(GridWarningLayout):



    def on_size(self, *args):
        self.on_status_color()


    def on_status_color(self, *args):

        if self.canvas is None:
            return

        self.canvas.before.clear()
        with self.canvas.before:
            Color(
                self.status_color[0],
                self.status_color[1],
                self.status_color[2],
                self.status_color[3]
            )
            Rectangle(
                pos=self.pos, 
                size=self.size
            )
