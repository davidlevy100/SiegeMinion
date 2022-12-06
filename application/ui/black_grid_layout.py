from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle

class BlackGridLayout(GridLayout):

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(
                pos=self.pos, 
                size=self.size
            )