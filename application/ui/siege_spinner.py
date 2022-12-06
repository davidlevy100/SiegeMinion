from kivy.uix.spinner import Spinner

from ui.siege_spinner_option import SiegeSpinnerOption
from ui.siege_dropdown import SiegeDropDown

class SiegeSpinner(Spinner):

    dropdown_cls = SiegeDropDown
    option_cls = SiegeSpinnerOption
    sync_height = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
