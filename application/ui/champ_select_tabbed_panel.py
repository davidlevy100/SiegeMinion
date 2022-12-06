from kivy.app import App
import kivy.properties as kp
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem, TabbedPanelHeader
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

from ui.activator_button import ActivatorButton

class BlackTabbedHeader(TabbedPanelHeader):

    background_color = (0,0,0,1)


class ColumnLabel(Label):

    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 0.8)
            Rectangle(pos=self.pos, size=self.size)


class ChampSelectTabbedPanelItem(BlackTabbedHeader):

    participant = kp.ObjectProperty()

    show_stats = kp.BooleanProperty(False)
    completed = kp.BooleanProperty(False)
    champion_name = kp.StringProperty("")

    button_active = kp.BooleanProperty(False)

    pick_rate = kp.StringProperty("")
    ban_rate = kp.StringProperty("")
    win_rate = kp.StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.content = GridLayout(rows=1)

        self.pick_rate_label = Label()
        self.ban_rate_label = Label()
        self.win_rate_label = Label()

        self.bind(pick_rate=self.pick_rate_label.setter('text'))
        self.bind(ban_rate=self.ban_rate_label.setter('text'))
        self.bind(win_rate=self.win_rate_label.setter('text'))

        for key, value in [
            ("Pick Rate", self.pick_rate_label),
            ("Ban Rate", self.ban_rate_label),
            ("Win Rate", self.win_rate_label),
        ]:

            this_column = GridLayout(cols=1)

            this_column.add_widget(
                ColumnLabel(text=key, size_hint_y = 0.8)
            )

            this_column.add_widget(value)

            self.content.add_widget(this_column)

        self.active_button = ActivatorButton(
            text="Take", 
            size_hint_x=0.5,
            disabled=True,
            on_press=self.button_action
        )
        self.bind(show_stats=self.active_button.setter('active'))
        self.content.add_widget(self.active_button)


    def on_completed(self, *args):
        self.active_button.disabled = not(self.completed)


    def button_action(self, *args):
        
        self.participant.toggle_stats()
    


class ChampSelectTabbedPanel(TabbedPanel):

    game_reset = kp.StringProperty()

    default_tab_cls = BlackTabbedHeader
    strip_border = 0

    background_color = (0, 0, 0, 0)
    #tab_pos = 'top_mid'

    participant = kp.ObjectProperty()

    champion = kp.DictProperty()
    champion_name = kp.StringProperty("")

    has_stats = kp.BooleanProperty(False)

    pick_rate = kp.StringProperty("")
    ban_rate = kp.StringProperty("")
    win_rate = kp.StringProperty("")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()
        self.app.bind(game_reset=self.setter('game_reset'))

        self.do_default_tab = True
        self.default_tab_cls = BlackTabbedHeader
        self.default_tab_text = "Champion Statistics"

        self.tab_height = 20
        self.tab_width = 200

        self.pick_ban_win_tab = ChampSelectTabbedPanelItem(
            text="Picks, Bans, Wins Stats"
        )

        self.bind(champion_name=self.pick_ban_win_tab.setter('champion_name'))
        self.pick_ban_win_tab.bind(button_active=self.setter('pbw_button_active'))


    def on_game_reset(self, *args):
        self.on_has_stats()


    def on_size(self, *args):
        self.tab_width = self.width / max(len(self.tab_list), 1)


    def on_participant(self, *args):
        self.participant.bind(pick_champion=self.setter('champion'))
        self.participant.bind(has_stats=self.setter('has_stats'))
        self.participant.bind(show_stats=self.pick_ban_win_tab.setter('show_stats'))

        self.participant.bind(pick_completed=self.pick_ban_win_tab.setter('completed'))
        self.participant.bind(pick_rate=self.pick_ban_win_tab.setter('pick_rate'))
        self.participant.bind(ban_rate=self.pick_ban_win_tab.setter('ban_rate'))
        self.participant.bind(win_rate=self.pick_ban_win_tab.setter('win_rate'))

        self.pick_ban_win_tab.participant = self.participant


    def on_champion(self, *args):
        self.champion_name = self.champion["external_name"]


    def on_has_stats(self, *args):

        for this_child in self.tab_list:
            if this_child is not self.default_tab:
                self.remove_widget(this_child)

        if self.has_stats:
            self.add_widget(self.pick_ban_win_tab)
            self.switch_to(self.pick_ban_win_tab)

        self.on_size()


    def on_pbw_button_active(self, *args):
        self.participant.toggle_stats()
