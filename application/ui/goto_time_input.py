import kivy.properties as kp

from ui.time_text_input import TimeTextInput

class GotoTimeInput(TimeTextInput):

    game_reset = kp.StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.bind(game_reset=self.setter('game_reset'))


    def on_game_reset(self, *args):
        self.milliseconds = 0


    def goto_time(self, *args):

        if self.milliseconds is not None:
            self.app.livestats_history.goto_time(self.milliseconds)
