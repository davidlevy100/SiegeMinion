from datetime import datetime
import json
from urllib.parse import urlencode, urlparse

from kivy.app import App
from kivy.event import EventDispatcher
from kivy.logger import Logger
from kivy.network.urlrequest import UrlRequest
import kivy.properties as kp

from data.slack.slack_dispatcher import SlackDispatcher

from configuration.vizcrank import ENDPOINTS, DEFAULT_HEADERS

class VizcrankSender(EventDispatcher):

    auto_slack = kp.BooleanProperty()
    auto_trio = kp.BooleanProperty()

    game_reset = kp.StringProperty("")

    section = kp.StringProperty("")

    trio_page_number = kp.StringProperty("")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()
        self.app.bind(game_reset=self.setter('game_reset'))


    def on_game_reset(self, *args):
        self.trio_page_number = ""


    def on_section(self, *args):

        self.auto_slack = bool(int(self.app.config.get(self.section, "auto_slack")))
        self.auto_trio = bool(int(self.app.config.get(self.section, "auto_trio")))

        self.app.config.add_callback(self.get_auto_slack, section=self.section, key="auto_slack")
        self.app.config.add_callback(self.get_auto_trio, section=self.section, key="auto_trio")

        self.slack_minion = SlackDispatcher(section=self.section)


    def can_process(self, *args):
        raise NotImplementedError


    def process_game_data(self, game_data, *args):
        raise NotImplementedError


    def get_auto_slack(self, *args):
        self.auto_slack = bool(int(self.app.config.get(self.section, "auto_slack")))


    def get_auto_trio(self, *args):
        self.auto_trio = bool(int(self.app.config.get(self.section, "auto_trio")))


    def has_field(self, **kwargs):

        """ Checks to see if we can apply data to Viz fields without error """

        return_value = False

        if ("field" in kwargs and
            "fields" in kwargs and
            "key" in kwargs
        ):
            field = kwargs["field"]
            fields = kwargs["fields"]
            key = kwargs["key"]

            if field in fields:
                if key in fields[field]:
                    return_value = True

        return return_value

    # REST Functions

    def get_url_and_headers(self, *args):

        raw_address = urlparse(self.app.config.get("Vizcrank", "ip"))
        address = max(raw_address.netloc, raw_address.path)
        port = self.app.config.get("Vizcrank", "port")

        host = f"{address}:{port}"

        url = f"http://{host}"

        headers = DEFAULT_HEADERS
        headers['Host'] = f"{address}:{port}"

        return url, headers


    def get_template(self, target_function, *args):

        url, headers = self.get_url_and_headers()

        endpoint = ENDPOINTS["template"]

        raw_params = {
            "media_sequencer": self.app.config.get(self.section, "media_sequencer"),
            "show": self.app.config.get(self.section, "show"),
            "template": self.app.config.get(self.section, "template")
        }
        
        params = urlencode(raw_params)

        full_url = f"{url}/{endpoint}?{params}"

        self.get_data(full_url, headers, target_function)


    def get_data(self, url, headers, target_function, *args):

        """ Single Function to GET data
            Expects full URL(url), headers(headers), 
            and the function
            to send data to (function)"""

        UrlRequest(
            url, 
            on_success = target_function, 
            on_redirect = self.got_redirect,
            on_failure = self.got_fail,
            on_error = self.got_error,
            req_headers = headers,
            verify = False
        )

    
    def post_data(self, url, headers, body, target_function, *args):

        """ Single Function to POST data
            Expects full URL(url), headers(headers), 
            and the function
            to send data to (function)"""


        UrlRequest(
            url, 
            on_success = target_function, 
            on_redirect = self.got_redirect,
            on_failure = self.got_fail,
            on_error = self.got_error,
            req_body = body,
            req_headers = headers,
            method = "POST",
            verify = False
        )


    def got_error(self, req, *args):
        Logger.exception(f"Vizcrank Error: {datetime.now().strftime('%r')} {req.url}, {args}")
        return


    def got_fail(self, req, *args):
        Logger.exception(f"Vizcrank Fail: {datetime.now().strftime('%r')} {req.url}, {args}")
        return


    def got_redirect(self, req, *args):
        Logger.exception(f"Vizcrank Redirect: {datetime.now().strftime('%r')} {req.url}, {args}")
        return


    def log_vizcrank_response(self, request, result, *args):

        LogMessage = f"Vizcrank Data Post: {datetime.now().strftime('%r')} {request.url}\n"
        
        vizcrank_response = "Sent Graphic to:\n"

        trio_page = ""

        if "mediasequencer" in result:
            vizcrank_response += f"Media Sequencer (Trio): {result['mediasequencer']}\n"

        if "showname" in result:
            vizcrank_response += f"Show: {result['showname']}\n"

        if "description" in result:
            vizcrank_response += f"{result['description']}\n".capitalize()

        if "pageassigned" in result:
            trio_page = result['pageassigned']
            vizcrank_response += f"Page: {trio_page}\n"

        vizcrank_response += "\n"

        self.trio_page_number = trio_page
        LogMessage += vizcrank_response
        Logger.info(LogMessage)
        
        return


    #Preview
    def get_preview(self, target_function, *args):
        self.get_template(target_function)

    
    #Slack
    def send_to_slack(self, *args):
        self.get_template(self.slack_handler)


    def slack_handler(self, request, result, *args):

        try:  
            finished_data = self.process_game_data(result)
            self.get_preview_image(finished_data, self.got_slack_image)

        except Exception as e:
            Logger.exception(f"Slack Error: {e}")

    
    def got_slack_image(self, request, result, **kwargs):
        self.slack_minion.send_image(result)


    # Trio
    def send_to_trio(self, *args):
        self.get_template(self.trio_handler)

    def trio_handler(self, request, result, *args):

        try:
            finished_data = self.process_game_data(result)
            self.post_to_trio(finished_data)

        except Exception as e:
            Logger.exception(f"Trio Error: {e}")


    def post_to_trio(self, data, *args):

        body = json.dumps(data)

        url, headers = self.get_url_and_headers()

        endpoint = ENDPOINTS["pages"]

        raw_params = {
            "media_sequencer": self.app.config.get(self.section, "media_sequencer"),
            "show": self.app.config.get(self.section, "show"),
            "template": self.app.config.get(self.section, "template"),
            "page": self.app.config.get(self.section, "page").strip(),
            "channel": self.app.config.get(self.section, "channel").strip(),
            "description": self.section
        }
        
        params = urlencode(raw_params)

        full_url = f"{url}/{endpoint}?{params}"

        self.post_data(
            full_url,
            headers,
            body,
            self.log_vizcrank_response
        )


    def get_preview_image(self, data, target_function, *args):

        data = json.dumps(data)
        url, headers = self.get_url_and_headers()

        endpoint = ENDPOINTS["previews"]

        raw_params = {
            "media_sequencer": self.app.config.get(self.section, "media_sequencer"),
            "show": self.app.config.get(self.section, "show"),
            "template": self.app.config.get(self.section, "template")
        }
        
        params = urlencode(raw_params)
        
        full_url = f"{url}/{endpoint}?{params}"

        self.post_data(
            full_url,
            headers,
            data,
            target_function
        )
