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

HEADERS = {
    'Accept': "application/json",
    'Cache-Control': "no-cache",
    'cache-control': "no-cache",
    'Host': "ddragon.leagueoflegends.com"
}

URL = "https://ddragon.leagueoflegends.com/api/versions.json"


class DDragonSettingOptions(SettingOptions):

    ''' Option Popup that allows scrolling content '''

    # name of function to call, should return a list of strings
    resource = kp.StringProperty()

    def __init__(self, *args, **kwargs):

        super().__init__(**kwargs)
        
        self.app = App.get_running_app()

        self.content = GridLayout(cols=1, spacing='5dp')

        self.scrollview = ScrollView(do_scroll_x=False)
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

        btn = Button(
            text='Cancel',
            size=(
                self.popup.width, 
                dp(50)
            ),
            size_hint=(0.9, None)
        )
        btn.bind(on_release=self.popup.dismiss)
        
        self.content.add_widget(btn)


    def _create_popup(self, instance):

        #we need to open the popup first to get the metrics
        self.popup.open()

        UrlRequest(
            URL, 
            on_success = self.got_success, 
            on_redirect = self.got_redirect,
            on_failure = self.got_fail,
            on_error = self.got_error,
            req_headers = HEADERS,
            verify = False
        )


    def on_options(self, *args, **kwargs):

        #Add some space on top
        self.content.add_widget(Widget(size_hint_y=None, height=dp(2)))

        # add all the options
        uid = str(self.uid)

        self.scrollcontent.clear_widgets()

        for option in self.options:
            state = 'down' if option == self.value else 'normal'
            btn = ToggleButton(
                text=option,
                state=state,
                group=uid,
                size=(self.popup.width, dp(55)),
                size_hint=(None, None)
            )
            btn.bind(on_release=self._set_option)
            self.scrollcontent.add_widget(btn)


    def got_success(self, request, result, **kwargs):

        self.options = result[:7]


    def got_error(self, req, *args):
        Logger.exception(f"DDragon Error: {datetime.now().strftime('%r')} {req.url}, {args}")
        return


    def got_fail(self, req, *args):
        Logger.exception(f"DDragon Fail: {datetime.now().strftime('%r')} {req.url}, {args}")
        return


    def got_redirect(self, req, *args):
        Logger.exception(f"DDragon Redirect: {datetime.now().strftime('%r')} {req.url}, {args}")
        return
