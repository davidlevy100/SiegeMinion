from ui.screens.hud_screen_manager import HUDScreenManager

class OverlayScreenManager(HUDScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(current=self.app.setter('current_overlay_screen'))


    def on_game_reset(self, *args):
        self.current = 'Champ Select'


    def set_screen(self, screen_name):
        self.current = screen_name
