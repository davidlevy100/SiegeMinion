from ui.time_text_input import TimeTextInput

class DelayInput(TimeTextInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.milliseconds = self.app.livestats_history.delay
        self.app.livestats_history.bind(delay=self.setter('milliseconds'))


    def update_delay(self, *args):
        self.app.livestats_history.set_delay(self.milliseconds)
