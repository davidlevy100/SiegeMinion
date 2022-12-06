from ui.screens.hud_screen_manager import HUDScreenManager

class StillScreenManager(HUDScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(current=self.app.setter('current_still_screen'))


    def on_game_reset(self, *args):
        self.current = "Caster Runes"


    def set_screen(self, screen_name):
        self.current = screen_name
