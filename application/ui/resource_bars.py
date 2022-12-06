from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
import kivy.properties as kp

class HorizontalBar(Widget):

    percent = kp.NumericProperty(1)

    def on_percent(self, *args):
        self.resize_bar()

    def on_size(self, *args):
        self.resize_bar()

    def resize_bar(self, *args):
        raise NotImplementedError



class HealthBar(HorizontalBar):

    def resize_bar(self, *args):

        self.canvas.before.clear()
        
        with self.canvas.before:

            #Green
            Color(rgb=[0.0, 1.0, 0.3])
            
            Rectangle(
                pos=self.pos, 
                size=((self.size[0] * self.percent), self.size[1])
            )


class ManaBar(HorizontalBar):

    def resize_bar(self, *args):

        self.canvas.before.clear()
        
        with self.canvas.before:

            #Blue
            Color(rgb=[0.3, 0.8, 1.0])
            
            Rectangle(
                pos=self.pos, 
                size=((self.size[0] * self.percent), self.size[1])
            )
