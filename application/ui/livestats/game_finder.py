from datetime import datetime
from urllib.parse import urlencode
from functools import partial

from kivy.app import App
from kivy.logger import Logger
import kivy.properties as kp
from kivy.network.urlrequest import UrlRequest

from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from kivy.graphics import Color, Rectangle

from ui.constants.text import GAMEFINDER_BUTTON_TEXT

GAME_TYPES = ["esportsGames", "platformGames"]


class GameFinderButton(Button):

    esports_games = kp.ListProperty([])
    all_games = kp.ListProperty([])
    platform_game_id = kp.StringProperty("")

    #Global Signal to Initialize
    game_reset = kp.StringProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()

        self.bind(platform_game_id=self.app.setter('platform_game_id'))

        self.text = GAMEFINDER_BUTTON_TEXT

        self.scroll_content = ScrollView(
            bar_width = 4,
            scroll_type=['bars', 'content']
        )

        self.main_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, None)
        )

        self.main_layout.bind(
            minimum_height=self.main_layout.setter('height')
        )

        self.esports_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            padding=10,
            spacing=10
        )

        self.esports_layout.bind(
            minimum_height=self.esports_layout.setter('height')
        )

        self.all_games_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            padding=10,
            spacing=10
        )

        self.all_games_layout.bind(
            minimum_height=self.all_games_layout.setter('height')
        )

        self.main_layout.add_widget(self.esports_layout)
        self.main_layout.add_widget(self.all_games_layout)

        self.scroll_content.add_widget(self.main_layout)
        
        self.popup = Popup(
            title='Livestats Games in Progress',
            content = self.scroll_content,
            size_hint=(0.8, 0.8)
        )


    def on_all_games(self, *args):

        self.all_games_layout.clear_widgets()

        if len(self.all_games) > 0:

            self.all_games_layout.add_widget(
                Label(
                    markup=True,
                    text="[size=24]All 10-Player Games[/size]",
                    size=(480, 40),
                    size_hint_y=None)
                )

            for this_game in self.all_games:

                if "participants" in this_game:
                    if (len(this_game["participants"]) == 10 and
                        "gameName" in this_game and
                        "platformGameId" in this_game
                    ):

                        game_name = this_game["gameName"]
                        platform_game_id = this_game["platformGameId"]

                        self.all_games_layout.add_widget(
                            Button(
                                text=f"{game_name:>64}    {platform_game_id:<64}",
                                size=(480, 40),
                                size_hint_y=None,
                                on_press=partial(
                                    self.game_selected,
                                    platform_game_id=platform_game_id
                                )
                            )
                        )

    def on_esports_games(self, *args):

        self.esports_layout.clear_widgets()

        if len(self.esports_games) > 0:

            self.esports_layout.add_widget(
                Label(
                    markup=True,
                    text="[size=24]Esports Games[/size]",
                    size=(480, 40),
                    size_hint_y=None
                )
            )

            for this_game in self.esports_games:

                self.esports_layout.add_widget(
                    Label(
                        markup=True,
                        text=f"[size=18]Esports Game ID: {this_game['esportsGameId']}[/size]",
                        size=(480, 40),
                        size_hint_y=None
                    )
                )

                for this_platform_game in this_game["platformGames"]:

                    game_name = this_platform_game["gameName"]
                    platform_game_id = this_platform_game["platformGameId"]

                    self.esports_layout.add_widget(
                        Button(
                            text=f"{game_name:>64}    {platform_game_id:<64}",
                            size=(480, 40),
                            size_hint_y=None,
                            on_press=partial(
                                self.game_selected,
                                platform_game_id=platform_game_id
                            )
                        )
                    )


    def on_press(self, *args):

        self.popup.open()
        self.get_games()


    def game_selected(self, *args, **kwargs):

        self.platform_game_id = kwargs["platform_game_id"]
        self.popup.dismiss(force=True)


    def on_game_reset(self, *args):
        self.initialize()

    
    def initialize(self, *args):

        self.platform_game_id = ""


    def get_games(self, **kwargs):

        try:

            config = self.get_config()
            base_url = config["base_url"]
            headers = config["headers"]
            querystring = {
                "state":"in_progress"
            }
            my_query = urlencode(querystring)

            for game_type in GAME_TYPES:

                url = f"{base_url}/{game_type}?{my_query}"

                self.get_data(
                    url=url,
                    headers=headers,
                    function=partial(
                        self.process_games,
                        game_type=game_type
                    )
                )

        except Exception as e:
            Logger.exception(f"Error: {e}")


    def process_games(self, request, result, **kwargs):

        if "game_type" in kwargs:
            
            if kwargs["game_type"] == "esportsGames":
                self.esports_games = result

            elif kwargs["game_type"] == "platformGames":
                self.all_games = result


    def get_config(self):

        base_url = self.app.config.get(
            'Livestats',
            'base_url'
        )

        if base_url[-1] == "/":
            base_url = base_url[:-1]

        api_key = self.app.config.get(
            'Livestats',
            'api_key'
        )

        headers = {
            'Accept': "application/json",
            'Cache-Control': "no-cache",
            'cache-control': "no-cache",
            'Connection': "keep-alive",
            'Host': "raw-stats-api.ewp.gg",
            'x-api-key': f"{api_key}"
        }

        return {
            "base_url": base_url,
            "headers": headers
        }
        

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
        self.myStatus = [0.5, 0, 0, 1]
        Logger.exception(f"Data Polling Error: {datetime.now().strftime('%r')} {req.url}, {args}")
        return


    def got_fail(self, req, *args):
        self.myStatus = [0.5, 0, 0, 1]
        Logger.exception(f"Data Polling Fail: {datetime.now().strftime('%r')} {req.url}, {args}")
        return


    def got_redirect(self, req, *args):
        Logger.exception(f"Data Polling Redirect: {datetime.now().strftime('%r')} {req.url}, {args}")
        return
