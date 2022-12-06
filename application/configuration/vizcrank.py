from datetime import datetime
from urllib.parse import urlencode, urlparse
from functools import partial
import json

from kivy.app import App
import kivy.properties as kp
from kivy.network.urlrequest import UrlRequest
from kivy.logger import Logger
from kivy.uix.settings import SettingOptions
from kivy.uix.settings import SettingSpacer
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.uix.label import Label


ENDPOINTS = {
    "media_sequencers": "v1/api/settings/vizcrank",
    "shows": "v1/api/resources/media_sequencer/shows",
    "templates": "v1/api/resources/media_sequencer/show/templates",
    "template": "v1/api/resources/media_sequencer/show/template",
    "previews": "v1/api/resources/media_sequencer/previews",
    "pages": "v1/api/resources/media_sequencer/show/pages"
}

DEFAULT_HEADERS = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    'Cache-Control': "no-cache",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
}


class VizcrankSettingOptions(SettingOptions):

    ''' Option Popup that allows scrolling content '''

    # name of function to call, should return a list of strings
    resource = kp.StringProperty()

    search_string = kp.StringProperty("")


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.app = App.get_running_app()

        self.content = GridLayout(cols=1, spacing='5dp')

        # Search Field
        self.search_field = TextInput(
            text="",
            hint_text="Search",
            size=(
                self.content.width, 
                dp(30)
            ),
            size_hint=(0.9, None)
        )

        self.search_field.bind(text=self.setter("search_string"))
        self.content.add_widget(self.search_field)

        self.scrollview = ScrollView(
            do_scroll_x=False
        )

        self.scrollcontent = GridLayout(
            cols=1,
            spacing='5dp',
            size_hint=(None, None)
        )

        self.scrollcontent.bind(
            minimum_height=self.scrollcontent.setter('height')
        )

        self.scrollview.add_widget(self.scrollcontent)
        self.content.add_widget(self.scrollview)
        self.content.add_widget(SettingSpacer())

        self.popup = Popup(
            content=self.content,
            title=self.title,
            size_hint=(0.5, 0.9),
            auto_dismiss=False
        )

        self.create_close_button()


    def on_options(self, *args, **kwargs):

        self.scrollcontent.clear_widgets()

        for option in self.options:

            if option.lower().startswith(self.search_string.lower()):

                state = 'down' if option == self.value else 'normal'
                btn = ToggleButton(
                    text=option,
                    state=state,
                    group=self.uid,
                    size=(self.popup.width, dp(55)),
                    size_hint=(None, None)
                )
                btn.bind(on_release=self._set_option)
                self.scrollcontent.add_widget(btn)


    def on_search_string(self, *args):

        if len(self.options) > 0:
            self.on_options()


    def create_close_button(self, *args):

        btn = Button(
            text = "Cancel",
            size = (
                self.popup.width, 
                dp(50)
            ),
            size_hint = (0.9, None)
        )
        btn.bind(on_release=self.popup.dismiss)
        
        self.content.add_widget(btn)


    def _create_popup(self, instance):

        #we need to open the popup first to get the metrics
        self.popup.open()

        if self.resource == "channels":
            channels = self.app.config.get("Vizcrank", "channels")
            self.options = channels.split(',')

        else:
            self.create_request()


    def create_request(self, *args):

        """ Returns url and headers """

        scheme = "http"

        raw_address = urlparse(self.app.config.get('Vizcrank', "ip"))

        if raw_address.scheme == 'https':
            scheme = "https"

        address = max(raw_address.netloc, raw_address.path)

        port = self.app.config.get("Vizcrank", "port")

        endpoint = ENDPOINTS[self.resource]

        raw_params = {}

        if self.resource == "shows":
            raw_params["media_sequencer"] = self.app.config.get(f"{self.section}", "media_sequencer")

        elif self.resource == "templates":
            raw_params["media_sequencer"] = self.app.config.get(f"{self.section}", "media_sequencer")
            raw_params["show"] = self.app.config.get(f"{self.section}", "show")
        
        params = urlencode(raw_params)

        headers = DEFAULT_HEADERS

        if scheme == "http":
            url = f"{scheme}://{address}:{port}/{endpoint}?{params}"
            headers['Host'] = f"{address}:{port}"
        else:
            url = f"{scheme}://{address}/{endpoint}?{params}"
            headers['Host'] = f"{address}"

        headers = DEFAULT_HEADERS
        

        self.get_data(
            url=url,
            headers=headers,
            function=self.process_resource
        )


    def get_data(self, **kwargs):

        """ Single Function to GET data
            Expects full URL(url), headers(headers), 
            and the function
            to send data to (function)"""

        try:
            
            url = kwargs["url"]
            headers = kwargs["headers"]
            function = kwargs["function"]


            UrlRequest(
                url, 
                on_success = function, 
                on_redirect = self.got_redirect,
                on_failure = self.got_fail,
                on_error = self.got_error,
                req_headers = headers,
                verify = False
            )

        except Exception as e:
            Logger.exception(f"Error: {e}")


    def got_error(self, req, *args):
        Logger.exception(f"Vizcrank Error: {datetime.now().strftime('%r')} {req.url}, {args}")
        return


    def got_fail(self, req, *args):
        Logger.exception(f"Vizcrank Fail: {datetime.now().strftime('%r')} {req.url}, {args}")
        return


    def got_redirect(self, req, *args):
        Logger.exception(f"Vizcrank Redirect: {datetime.now().strftime('%r')} {req.url}, {args}")
        return


    def process_resource(self, request, result, **kwargs):

        options = []

        if self.resource in result:
            
            if self.resource == "templates":
                options = [x["title"] for x in result[self.resource]]
                
            else:
                options = [x["name"] for x in result[self.resource]]

        else:
            Logger.exception(f"Vizcrank Resource Error: {datetime.now().strftime('%r')} resource not recognized")

        options.sort()
        self.options = options


    



