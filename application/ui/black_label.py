from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class BlackLabel(Label):

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(
                pos=self.pos, 
                size=self.size
            )