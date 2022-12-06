from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
import kivy.properties as kp

from ui.constants.images import APP_BACKGROUND

class RootLayout(GridLayout):

    background_image = kp.StringProperty(APP_BACKGROUND)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
