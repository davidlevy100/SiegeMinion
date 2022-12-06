import kivy.properties as kp

from data.events.data_event_dispatch import DataEventDispatcher


class BottomBarVizSender(DataEventDispatcher):

    current_title = kp.StringProperty()
    patch = kp.StringProperty()
    date = kp.StringProperty()

    scoreboard = kp.BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.current_title = self.app.bottom_bar.current_title
        self.app.bottom_bar.bind(current_title=self.setter('current_title'))

        self.patch = self.app.bottom_bar.patch
        self.app.bottom_bar.bind(patch=self.setter('patch'))
        
        self.date = self.app.bottom_bar.date
        self.app.bottom_bar.bind(date=self.setter('date'))

        self.app.bottom_bar.bind(update_now=self.setter('update_now'))
        self.bind(output=self.app.vizrt.setter('input_data'))

        self.scoreboard = self.app.observer_ui_poller.scoreboard
        self.app.observer_ui_poller.bind(scoreboard=self.setter('scoreboard'))


    def on_current_title(self, *args):

        output = {
            "ov/titleb": self.current_title
        }

        self.send_data(**output)


    def on_date(self, *args):

        output = {
            "ov/date": self.date
        }

        self.send_data(**output)


    def on_patch(self, *args):

        output = {
            "ov/patch": self.patch
        }

        self.send_data(**output)


    def on_scoreboard(self, *args):

        output = {
            "ov/tabDown": int(self.scoreboard)
        }

        self.app.vizrt.send_now(output)


    def on_update_now(self, *args):

        output = {
            "ov/date": self.date,
            "ov/patch": self.patch,
            "ov/titleb": self.current_title
        }

        self.app.vizrt.send_now(output)


    def on_game_reset(self, *args):

        self.on_update_now()
