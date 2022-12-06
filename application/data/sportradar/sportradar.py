from datetime import datetime
from urllib.parse import urlencode
from urllib.parse import urlparse

from kivy.app import App
import kivy.properties as kp
from kivy.logger import Logger
from kivy.network.urlrequest import UrlRequest

from data.events.data_event_dispatch import DataEventDispatcher


class Sportradar(DataEventDispatcher):

    picks_bans_wins = kp.DictProperty(allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def on_game_reset(self, *args):

        self.update_picks_bans_wins()


    def get_config(self):

        try:

            base_url = self.app.config.get(
                'Sportradar',
                'base_url'
            )

            if base_url[-1] == "/":
                base_url = base_url[:-1]

            api_key = self.app.config.get(
                'Sportradar',
                'api_key'
            )

            headers = {
                'Authorization': f"{api_key}",
                'Content-Type': "application/json",
                'Accept': "application/json",
                'Cache-Control': "no-cache",
                'accept-encoding': "gzip, deflate",
                'Connection': "keep-alive",
                'cache-control': "no-cache"
            }

            return base_url, headers

        except Exception as e:
            Logger.exception(f"Error: {e}")
            return None, None

    
    def update_picks_bans_wins(self, *args):

        base_url, headers = self.get_config()

        if (base_url is not None and
            headers is not None
        ):

            report  = self.app.config.get(
                'Sportradar',
                'champion_stats'
            )

            querystring = {
                "limit":"null",
                "dataFormat":"raw"
            }

            my_query = urlencode(querystring)

            url = f"{base_url}/{report}?{my_query}"

            self.get_data(
                url=url,
                headers=headers,
                function=self.process_picks_bans_wins
            )

        else:
            self.picks_bans_wins = None


    def process_picks_bans_wins(self, request, result, *args):

        """ Expects Sportradar Report (result) including
            Picks, Bans, Wins, League and Split """

        try:

            column_indexes = {}

            for index, column_name in enumerate(result["columns"]):

                if "name" in column_name:
                    column_indexes[column_name["name"]] = index

            pbw_table = {}

            champ_name_index = column_indexes["Champion"]
            pick_index = column_indexes["Picks"]

            picks = 0

            for this_champ in result["data"]:

                champ_name = this_champ[champ_name_index]
                picks += this_champ[pick_index]

                this_champ_data = {}

                for key, value in column_indexes.items():
                    this_champ_data[key] = this_champ[value]

                pbw_table[champ_name] = this_champ_data

            if len(pbw_table) > 0:
                first_champ = list(pbw_table.keys())[0]

                if "League" in pbw_table[first_champ]:
                    pbw_table["League"] = pbw_table[first_champ]["League"]

                if "Season" in pbw_table[first_champ]:
                    pbw_table["Season"] = pbw_table[first_champ]["Season"]

            pbw_table["total games"] = picks // 10

            self.picks_bans_wins = pbw_table

        except Exception as e:
            Logger.exception(f"Error: {e}")
            self.picks_bans_wins = None

        return


    def get_data(self, **kwargs):

        """ Single Function to GET data from Sportradar
            Expects full URL(url), headers(headers), and the function
            to send data to (function)"""

        if ("url" in kwargs and
            "headers" in kwargs and
            "function" in kwargs
        ):

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
        
    
    def got_error(self, req, *args):
        Logger.exception(f"Sportradar Error: {datetime.now().strftime('%r')} {req.url}, {args}")
        return


    def got_fail(self, req, *args):
        Logger.exception(f"Sportradar Fail: {datetime.now().strftime('%r')} {req.url}, {args}")
        return


    def got_redirect(self, req, *args):
        Logger.exception(f"Sportradar Redirect: {datetime.now().strftime('%r')} {req.url}, {args}")
        return
