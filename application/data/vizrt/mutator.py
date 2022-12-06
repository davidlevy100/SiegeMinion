import kivy.properties as kp

from data.events.data_event_dispatch import DataEventDispatcher


ALT_LOGO_SUFFIX = "_alt"


class VizMutator(DataEventDispatcher):

    tricode_left = kp.StringProperty()
    tricode_right = kp.StringProperty()

    use_alt_logo_left = kp.BooleanProperty()
    use_alt_logo_right = kp.BooleanProperty()

    viz_logo_left = kp.StringProperty()
    viz_logo_right = kp.StringProperty()

    logo_map = kp.DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.game_data.bind(tricode_left=self.setter('tricode_left'))
        self.app.game_data.bind(tricode_right=self.setter('tricode_right'))
        

        self.bind(output=self.app.vizrt.setter('input_data'))


    def on_game_reset(self, *args):

        self.set_logo("left", "normal")
        self.set_logo("right", "normal")

        self.logo_mutator = ""


    def on_tricode_left(self, *args):

        if self.use_alt_logo_left:
            self.viz_logo_left = f"{self.tricode_left}{ALT_LOGO_SUFFIX}"
        else:
            self.viz_logo_left = f"{self.tricode_left}"


    def on_tricode_right(self, *args):
        if self.use_alt_logo_right:
            self.viz_logo_right = f"{self.tricode_right}{ALT_LOGO_SUFFIX}"
        else:
            self.viz_logo_right = f"{self.tricode_right}"



    def set_logo(self, side, state):

        use_alt = False

        if state == "down":
            use_alt = True

        if side == "left":
            self.use_alt_logo_left = use_alt
            self.on_tricode_left()

        if side == "right":
            self.use_alt_logo_right = use_alt
            self.on_tricode_right()



