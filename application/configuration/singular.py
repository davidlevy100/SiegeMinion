from datetime import datetime
from urllib.parse import urlencode, urlparse
from functools import partial
from operator import itemgetter
import json
from base64 import urlsafe_b64encode, urlsafe_b64decode

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

from configuration.password_settings import PasswordString


DEFAULT_HEADERS = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    'Cache-Control': "no-cache",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
}


class SingularPassword(PasswordString):

    def _validate(self, instance):
        self._dismiss()
        value = self.textinput.text.strip()
        self.value = urlsafe_b64encode(value.encode()).decode('utf-8')


class SingularButton(ToggleButton):

    data = kp.DictProperty({})


class SingularSettingOptions(SettingOptions):

    ''' Option Popup that allows scrolling content '''

    # name of function to call, should return a list of strings
    #resource = kp.StringProperty()

    breadcrumbs = kp.ListProperty([])
    folder = kp.StringProperty("root")
    search_string = kp.StringProperty("")

    def __init__(self, *args, **kwargs):

        super().__init__(**kwargs)
        
        self.app = App.get_running_app()

        self.content = GridLayout(cols=1, spacing='5dp')

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


    def _set_option(self, instance):

        paths = {
            "default_normal_team_image": "normal_team_image_folder",
            "default_white_team_image": "white_team_image_folder",
            "default_player_image": "player_image_folder", 
            "default_champion_icon_image": "champion_icon_folder",
            "default_champion_splash_image": "champion_splash_folder",
            "default_item_image": "item_image_folder",
            "default_rune_image": "rune_image_folder",
            "default_summoner_image": "summoner_spell_image_folder",
            "default_game_icon_image": "game_icon_folder"
        }

        self.value = instance.data["fid"]
        self.popup.dismiss()

        path = paths[self.key]

        #set corresponding directory
        self.app.config.set("Singular", path, self.folder)
        self.app.config.write()

        self.options.clear()
        self.search_field.text = ""
        self.breadcrumbs.clear()


    def _create_popup(self, instance):

        #we need to open the popup first to get the metrics
        self.popup.open()
        self.navigate_down()


    def on_search_string(self, *args):

        if len(self.options) > 0:
            self.on_options()


    def on_options(self, *args, **kwargs):

        # add all the options
        self.scrollcontent.clear_widgets()

        if len(self.breadcrumbs) > 1:

            parent_btn = ToggleButton(
                text = "../",
                group = f"{self.uid}",
                size = (self.popup.width, dp(55)),
                size_hint = (None, None)
            )
            
            parent_btn.bind(on_release=self.navigate_up)
            self.scrollcontent.add_widget(parent_btn)

        self.create_elements()

    
    def create_elements(self, *args):

        for option in self.options:

            if option["name"].startswith(self.search_string):

                state = 'down' if option["fid"] == self.value else 'normal'

                btn = SingularButton(
                    data = option,
                    state = state,
                    group = f"{self.uid}",
                    size = (self.popup.width, dp(55)),
                    size_hint = (None, None)
                )

                if option["type"] == "fo":
                
                    btn.text = f"{option['name']}/"
                    btn.bind(on_release=partial(
                        self.navigate_down,
                        folder=option["fid"]
                        )
                    )

                else:
                    btn.text = f"{option['name']}"
                    btn.bind(on_release=self._set_option)

                self.scrollcontent.add_widget(btn)


    def navigate_down(self, *args, folder="root"):

        self.folder = folder
        self.breadcrumbs.append(folder)

        self.create_request(folder=folder)

    
    def navigate_up(self, *args):

        if len(self.breadcrumbs) > 1:
            self.breadcrumbs.pop()
            self.folder = self.breadcrumbs[-1]

        else:
            self.folder = "root"

        self.create_request(folder=self.folder)

    def create_request(self, *args, folder="root"):

        """ Returns url and headers """

        user_name = self.app.config.get("Singular", "user_name")
        password = urlsafe_b64decode(
            self.app.config.get("Singular", "password").encode()
        ).decode('utf-8')

        auth = urlsafe_b64encode(f"{user_name}:{password}".encode())

        url = f"https://app.singular.live/apiv1/dashboard/folder/{folder}/elements"

        headers = {}
        headers['Authorization'] = f"Basic {auth.decode('utf-8')}"

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


    def got_error(self, req, result, *args):
        Logger.exception(f"Singular Error: {datetime.now().strftime('%r')} {req.url}")
        self.scrollcontent.clear_widgets()

        self.scrollcontent.add_widget(
            Label(text=result)
        )
        return


    def got_fail(self, req, result, *args):
        Logger.exception(f"Singular Fail: {datetime.now().strftime('%r')} {req.url}")

        self.scrollcontent.clear_widgets()

        self.scrollcontent.add_widget(
            Label(text=result)
        )
        
        return


    def got_redirect(self, req, *args):
        Logger.exception(f"Singular Redirect: {datetime.now().strftime('%r')} {req.url}, {args}")
        return


    def process_resource(self, request, result, **kwargs):

        folders = []
        images = []

        for this_element in result:

            if "type" in this_element:
                if this_element["type"] == "fo":
                    folders.append(this_element)

                elif this_element["type"] == "i":
                    images.append(this_element)

        new_folders = sorted(
            folders, 
            key=itemgetter('name')
        )
        
        new_images = sorted(
            images, 
            key=itemgetter('name')
        )

        self.options = [*new_folders, *new_images]


class SingularFolderSettingOptions(SingularSettingOptions):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        self.close_btn_text = "Select this folder"

    def create_close_button(self, *args):

        btn = Button(
            text = "Select this folder",
            size = (
                self.popup.width, 
                dp(50)
            ),
            size_hint = (0.9, None)
        )
        btn.bind(on_release=self._set_option)
        
        self.content.add_widget(btn)

    
    def _set_option(self, instance):

        self.value = self.breadcrumbs[-1]
        self.popup.dismiss()

        self.options.clear()
        self.search_field.text = ""
        self.breadcrumbs.clear()


    def create_elements(self, *args):

        for option in self.options:

            if (option["type"] == "fo" and
                option["name"].startswith(self.search_string)
            ):

                state = 'down' if option["fid"] == self.value else 'normal'

                element = SingularButton(
                    data = option,
                    state = state,
                    group = f"{self.uid}",
                    size = (self.popup.width, dp(55)),
                    size_hint = (None, None)
                )
                
                element.text = f"{option['name']}/"
                element.bind(on_release=partial(
                    self.navigate_down,
                    folder=option["fid"]
                    )
                )

            else:
                element = Label(
                    text = f"{option['name']}",
                    size=(self.popup.width, dp(55)),
                    size_hint=(None, None)
                )

            self.scrollcontent.add_widget(element)
