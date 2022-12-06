from kivy.app import App
from kivy.event import EventDispatcher
import kivy.properties as kp
from kivy.logger import Logger

from ui.constants.colors import STATUS_OPTIONS

class EngineDispatcher(EventDispatcher):

    input_data = kp.DictProperty()
    dispatch_type = kp.StringProperty("")
    connected = kp.BooleanProperty(False)
    status = kp.OptionProperty(STATUS_OPTIONS[0], options=STATUS_OPTIONS)

    app = None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()


    def on_input_data(self, *args):

        message = self.construct_message(**args[1])
        self.update_engine(message)


    def on_connected(self, *args):

        if self.connected:
            self.get_config()
            self.open_connection()

        else:
            self.close_connection()


    def send_now(self, message, *args):

        message = self.construct_message(**message)
        self.update_engine(message)


    def construct_message(self, *args, **kwargs):
        raise NotImplementedError

    def get_config(self, *args):
        raise NotImplementedError

    def open_connection(self, *args):
        raise NotImplementedError

    def close_connection(self, *args):
        raise NotImplementedError

    def update_engine(self, message, *args):
        raise NotImplementedError

    def reset_engine(self, *args):
        raise NotImplementedError
