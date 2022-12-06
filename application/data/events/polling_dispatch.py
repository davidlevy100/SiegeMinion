from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.network.urlrequest import UrlRequest
import kivy.properties as kp
from kivy.logger import Logger

from ui.constants.colors import STATUS_OPTIONS


class PollingDispatcher(EventDispatcher):

    #Global Signal to Initialize
    game_reset = kp.StringProperty(None)

    enabled = kp.BooleanProperty(True)

    connected = kp.BooleanProperty(False)
    output = kp.DictProperty()
    dispatch_type = kp.StringProperty("")

    status = kp.OptionProperty(STATUS_OPTIONS[0], options=STATUS_OPTIONS)

    app = None
    full_url = None
    headers = None
    run_event = None
    server_url = None
    server_port = None
    token = None
    update_interval = None

    game_over = kp.BooleanProperty(False)
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()


    def on_connected(self, *args):

        if (self.connected and
            self.run_event is None
        ):
            Logger.info(f"Data Poller Connected: {datetime.now().strftime('%r')}")
            self.construct_request()
            self.run_event = Clock.schedule_interval(self.get_data, self.update_interval)

        else:
            self.initialize()


    def on_output(self, *args):
        self.status = "good"


    def on_game_reset(self, *args):
        self.initialize()
            

    def reschedule(self, *args):

        if (self.connected and 
            self.run_event is None
        ):
            self.run_event = Clock.schedule_interval(
                self.get_data,
                self.update_interval
            )


    def construct_request(self):
        raise NotImplementedError


    def initialize(self, *args):

        #self.connected = False
        self.output.clear()
        self.status = "off"

        self.full_url = None
        self.headers = None

        if self.run_event is not None:
            self.run_event.cancel()
            self.run_event = None

        Logger.info(f"Disconnected: {datetime.now().strftime('%r')}")


    def get_data(self, dt):

        if not self.game_over:
            UrlRequest(
                self.full_url, 
                on_success=self.handle_request, 
                on_redirect=self.got_redirect,
                on_failure=self.got_fail,
                on_error=self.got_error,
                req_headers=self.headers,
                verify=False
            )


    def handle_request(self, request, result):

        if self.connected:
            self.output = result

    
    def got_error(self, req, *args):

        if self.connected:
            self.status = "bad"
        Logger.exception(f"Data Polling Error: {datetime.now().strftime('%r')} {req.url}, {args}")

        if (self.connected and
            self.run_event is not None
        ):
            self.run_event.cancel()
            self.run_event = None

            Clock.schedule_once(self.reschedule, 1.0)


    def got_fail(self, req, *args):

        if self.connected:
            self.status = "bad"
        Logger.exception(f"Data Polling Fail: {datetime.now().strftime('%r')} {req.url}, {args}")


    def got_redirect(self, req, *args):

        if self.connected:
            self.status = "warning"
        Logger.exception(f"Data Polling Redirect: {datetime.now().strftime('%r')} {req.url}, {args}")
