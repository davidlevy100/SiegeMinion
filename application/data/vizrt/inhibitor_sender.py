import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher


class InhibitorVizSender(DataEventDispatcher):

    top_source = kp.ObjectProperty()
    mid_source = kp.ObjectProperty()
    bot_source = kp.ObjectProperty()

    side = kp.StringProperty()

    # Input Properties

    tricode = kp.StringProperty("")

    top_active = kp.BooleanProperty(True)
    top_timer = kp.NumericProperty(0)
    top_timer_string = kp.StringProperty("---")

    mid_active = kp.BooleanProperty(True)
    mid_timer = kp.NumericProperty(0)
    mid_timer_string = kp.StringProperty("---")

    bot_active = kp.BooleanProperty(True)
    bot_timer = kp.NumericProperty(0)
    bot_timer_string = kp.StringProperty("---")

    # Output Properties
    active = kp.BooleanProperty()

    anim_state = kp.NumericProperty(0)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(output=self.app.vizrt.setter('input_data'))
        self.check_active()

        if self.side == "blue":
            self.tricode = self.app.top_bar.tricode_left
            self.app.top_bar.bind(tricode_left=self.setter('tricode'))
        else:
            self.tricode = self.app.top_bar.tricode_right
            self.app.top_bar.bind(tricode_right=self.setter('tricode'))


    def on_top_source(self, *args):

        self.top_source.bind(active=self.setter('top_active'))
        self.top_source.bind(timer=self.setter('top_timer'))
        self.top_source.bind(timer_string=self.setter('top_timer_string'))


    def on_mid_source(self, *args):

        self.mid_source.bind(active=self.setter('mid_active'))
        self.mid_source.bind(timer=self.setter('mid_timer'))
        self.mid_source.bind(timer_string=self.setter('mid_timer_string'))


    def on_bot_source(self, *args):

        self.bot_source.bind(active=self.setter('bot_active'))
        self.bot_source.bind(timer=self.setter('bot_timer'))
        self.bot_source.bind(timer_string=self.setter('bot_timer_string'))
    

    def check_active(self, *args):
        self.active = not (self.top_active and self.mid_active and self.bot_active)

    def on_top_active(self, *args):
        self.check_active()

    def on_mid_active(self, *args):
        self.check_active()

    def on_bot_active(self, *args):
        self.check_active()

    
    def on_anim_state(self, *args):

        self.send_all_inhibs()


    def on_top_timer_string(self, *args):

        self.send_all_inhibs()


    def on_mid_timer_string(self, *args):

        self.send_all_inhibs()


    def on_bot_timer_string(self, *args):

        self.send_all_inhibs()


    def on_game_reset(self, *args):

        output = {
            f"inhib/{self.side}/tri": self.tricode,
            f"inhib/{self.side}/top/inhib": int(self.top_active),
            f"inhib/{self.side}/top/cd": self.top_timer_string,
            f"inhib/{self.side}/mid/inhib": int(self.mid_active),
            f"inhib/{self.side}/mid/cd": self.mid_timer_string,
            f"inhib/{self.side}/bot/inhib": int(self.bot_active),
            f"inhib/{self.side}/bot/cd": self.bot_timer_string,
            "inhib/sel": 0
        }

        self.app.vizrt.send_now(output)


    def send_all_inhibs(self, *args):

        output = {
            f"inhib/{self.side}/tri": self.tricode,
            f"inhib/{self.side}/top/inhib": int(self.top_active),
            f"inhib/{self.side}/top/cd": self.top_timer_string,
            f"inhib/{self.side}/mid/inhib": int(self.mid_active),
            f"inhib/{self.side}/mid/cd": self.mid_timer_string,
            f"inhib/{self.side}/bot/inhib": int(self.bot_active),
            f"inhib/{self.side}/bot/cd": self.bot_timer_string,
            "inhib/sel": self.anim_state
        }

        self.send_data(**output)



class InhibitorVizController(DataEventDispatcher):

    left_active = kp.BooleanProperty(False)
    right_active = kp.BooleanProperty(False)

    anim_state = kp.NumericProperty(0)

    visible = kp.BooleanProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.vizrt.setter('input_data'))

        self.app.inhib_left_viz_sender.bind(active=self.setter('left_active'))
        self.app.inhib_right_viz_sender.bind(active=self.setter('right_active'))

        self.bind(anim_state=self.app.inhib_left_viz_sender.setter('anim_state'))
        self.bind(anim_state=self.app.inhib_right_viz_sender.setter('anim_state'))

        self.visible = self.app.config.getboolean("User Game Data", "inhibitors")
        self.app.config.add_callback(self.check_visible, "User Game Data", "inhibitors")


    def on_left_active(self, *args):
        self.check_active()


    def on_right_active(self, *args):
        self.check_active()


    def on_game_reset(self, *args):

        output = {
            "inhib/show": int(bool(self.visible)),
        }

        self.app.vizrt.send_now(output)


    def check_active(self, *args):

        state = 0

        if (self.left_active and 
            self.right_active
        ):
            state = 3

        elif self.left_active:
            state = 1

        elif self.right_active:
            state = 2

        self.anim_state = state


    def on_visible(self, *args):

        output = {
            "inhib/show": int(bool(self.visible))
        }

        self.send_data(**output)


    def toggle_visible(self, *args):

        self.visible = not(self.visible)

        LogMessage = (
            f"Overlay: Inhibitors visible: {self.visible}"
        )
        Logger.info(LogMessage)


    def check_visible(self, *args):
        
        self.visible = self.app.config.getboolean("User Game Data", "inhibitors")
