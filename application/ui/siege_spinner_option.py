from kivy.uix.spinner import SpinnerOption

class SiegeSpinnerOption(SpinnerOption):

    background_color = [0.25, 0.25, 0.25, 1.0]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

