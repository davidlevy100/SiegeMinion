from kivy.app import App

from kivy.uix.gridlayout import GridLayout
import kivy.properties as kp
from kivy.uix.textinput import TextInput

from ui.integer_input import IntegerInput


class WinsInput(IntegerInput):

    side = kp.StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()


    def on_value(self, *args):
        super().on_value(args)

        self.app = App.get_running_app()

        self.app.top_bar.update_wins(
            self.side, self.text
        )


class RecordInput(TextInput):

    side = kp.StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()

        self.hint_text = "record"
        self.multiline = False
        self.write_tab = False
        self.padding = 4, 0

    
    def on_size(self, *args):
        self.font_size = self.size[1] * 0.8


    def on_text(self, *args):

        self.app.top_bar.update_record(
            self.side, self.text
        )


class WinRecordLayout(GridLayout):

    side = kp.StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()
        self.rows = 1
        self.size_hint_y = 0.8


    def on_side(self, *args):

        self.record_input = RecordInput(side=self.side)
        self.wins_input = WinsInput(side=self.side)

        self.app.config.add_callback(
            self.check_win_or_record,
            section = "User Game Data",
            key="win_or_record"
        )

        self.check_win_or_record()


    def check_win_or_record(self, *args):

        win_or_record = self.app.config.get(
            "User Game Data",
            "win_or_record",
        )
        
        self.clear_widgets()

        if win_or_record == "Wins":
            self.add_widget(self.wins_input)
        elif win_or_record == "Record":
            self.add_widget(self.record_input)
