import json

from kivy.app import App
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.network.urlrequest import UrlRequest
import kivy.properties as kp
from kivy.logger import Logger

from ui.constants.colors import STATUS_OPTIONS

from configuration.defaults import get_defaults


HEADERS = {'Content-type': 'application/json'}

class EsportsDispatcher(EventDispatcher):

    #Global Signal to Initialize
    game_reset = kp.StringProperty(None)
    paused = kp.BooleanProperty(False)

    esports_server_status = kp.OptionProperty(STATUS_OPTIONS[0], options=STATUS_OPTIONS)


    esports_server_url = kp.StringProperty("")
    enabled = kp.BooleanProperty(False)
    poll_interval = kp.NumericProperty(0.1)

    run_event = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()
        self.app.bind(game_reset=self.setter('game_reset'))

        self.get_settings()
        

    def get_settings(self, *args):

        raise NotImplementedError
        

    def on_game_reset(self, *args):
        self.initialize()


    def on_paused(self, *args):

        if ((not self.paused) and
            self.enabled and
            self.run_event is None
        ):
            Logger.info(f"Sync Poller Connected")
            self.run_event = Clock.schedule_interval(self.get_data, self.poll_interval)

        else:
            self.initialize()


    def toggle_enabled(self, *args):

        self.enabled = not self.enabled
            

    def reschedule(self, *args):

        if (not self.paused and 
            self.run_event is None
        ):
            self.run_event = Clock.schedule_interval(
                self.get_data,
                self.poll_interval
            )


    def initialize(self, *args):

        self.esports_server_status = STATUS_OPTIONS[0]
        self.server_time = 0
        self.server_delay = 0

        if self.run_event is not None:
            self.run_event.cancel()
            self.run_event = None

        Logger.info(f"Disconnected")


    def get_data(self, dt):

        if ((not self.paused) and
            self.enabled
        ):
            UrlRequest(
                self.esports_server_url, 
                on_success=self.server_success, 
                on_redirect=self.server_redirect,
                on_failure=self.server_fail,
                on_error=self.server_error,
                req_headers=HEADERS,
                verify=False
            )

    def server_success(self, request, result):

        self.esports_server_status = "good"


    def server_error(self, req, *args):

        if not self.paused:
            self.esports_server_status = "bad"
            Logger.exception(f"Esports Sync Polling Error: {req.url}, {args}")


    def server_fail(self, req, *args):
        
        if not self.paused:
            self.esports_server_status = "bad"
            Logger.exception(f"Esports Sync Polling Fail: {req.url}, {args}")


    def server_redirect(self, req, *args):
        
        if not self.paused:
            self.esports_server_status = "warning"
            Logger.exception(f"Esports Sync Polling redirect: {req.url}, {args}")


class SyncDispatcher(EsportsDispatcher):

    sync_offset = kp.NumericProperty(0.0)
    server_time = kp.NumericProperty(0)
    server_delay = kp.NumericProperty(0)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.config.add_callback(self.get_settings, section="Sync")


    def get_settings(self, *args):

        self.esports_server_url = self.app.config.getdefault("Sync", "url", "")
        self.enabled = bool(self.app.config.getdefaultint("Sync", "enabled", 0))
        self.poll_interval = self.app.config.getdefault("Sync", "poll_interval", 0.2)
        self.sync_offset = self.app.config.getdefaultint("Sync", "sync_offset", 0)


    def server_success(self, request, result):

        if "current_delay" in result:
            self.server_time = int(float(result["current_delay"])) + self.sync_offset

        if ("length" in result and
            "time" in result
        ):
            self.server_delay = int((result["length"] - result["time"]) * 1000)

        self.esports_server_status = "good"




class ObserverUIDispatcher(EsportsDispatcher):

    scoreboard = kp.BooleanProperty(True)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.config.add_callback(self.get_settings, section="Observer UI")

    
    def initialize(self, *args):

        super().initialize()
        self.scoreboard = True


    def get_settings(self, *args):

        self.esports_server_url = self.app.config.getdefault("Observer UI", "url", "")
        self.enabled = bool(self.app.config.getdefaultint("Observer UI", "enabled", 0))
        self.poll_interval = self.app.config.getdefault("Observer UI", "poll_interval", 0.2)

        if self.enabled:
            self.enabled = self.app.sync_poller.enabled
            self.app.sync_poller.bind(enabled=self.setter('enabled'))

            self.paused = self.app.sync_poller.paused
            self.app.sync_poller.bind(paused=self.setter('paused'))


    def server_success(self, request, result):

        if "interfaceScoreboard" in result:
            self.scoreboard = bool(result["interfaceScoreboard"])

        self.esports_server_status = "good"
