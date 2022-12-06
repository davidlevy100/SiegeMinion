from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Rectangle

class SiegeDropDown(DropDown):

    max_height = 800
    bar_width = 8

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)

    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
