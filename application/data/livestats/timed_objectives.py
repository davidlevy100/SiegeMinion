from datetime import datetime

from kivy.clock import Clock
import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher

INHIBITOR_TIME = 300000

class InhibitorsDispatcher(DataEventDispatcher):

    # Input Data
    inhibitor_event = kp.DictProperty()

    #Inhibitors
    top_100 = kp.NumericProperty(None, allownone=True)
    mid_100 = kp.NumericProperty(None, allownone=True)
    bot_100 = kp.NumericProperty(None, allownone=True)

    top_200 = kp.NumericProperty(None, allownone=True)
    mid_200 = kp.NumericProperty(None, allownone=True)
    bot_200 = kp.NumericProperty(None, allownone=True)

    blue_inhib_kills = kp.ListProperty()
    red_inhib_kills = kp.ListProperty()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.live_data.bind(inhibitor_event=self.setter('inhibitor_event'))
        self.update_output()


    def on_game_reset(self, *args):

        self.top_100 = None
        self.mid_100 = None
        self.bot_100 = None

        self.top_200 = None
        self.mid_200 = None
        self.bot_200 = None

        self.blue_inhib_kills.clear()
        self.red_inhib_kills.clear()

        self.update_output()

    
    def on_inhibitor_event(self, *args):

        if ("gameTime" in self.inhibitor_event and
            "teamID" in self.inhibitor_event and
            "lane" in self.inhibitor_event
        ):

            lane = self.inhibitor_event["lane"]
            teamID = self.inhibitor_event["teamID"]
            game_time = self.inhibitor_event["gameTime"]
            
            propname = f"{lane}_{teamID}"

            if propname in self.properties():

                this_prop = self.property(propname)
                this_prop.set(self, game_time)

                self.update_output()

                owning_team = ""

                if self.inhibitor_event["teamID"] == 100:

                    self.red_inhib_kills.append(game_time)

                    owning_team = "Blue "

                elif self.inhibitor_event["teamID"] == 200:

                    self.blue_inhib_kills.append(game_time)

                    owning_team = "Red "

                game_time_string = datetime.utcfromtimestamp(game_time/1000).strftime("%H:%M:%S")

                LogMessage = (
                    f"Game Event: {datetime.now().strftime('%r')} "
                    f"{owning_team}{lane} inhibitor "
                    f"destroyed at gametime: {game_time_string}"
                )

                Logger.info(LogMessage)

            else:

                Logger.exception(f"Data Error: Property {propname} not found")  

    
    def update_output(self, *args):

        data = {
            "top_100": self.top_100,
            "mid_100": self.mid_100,
            "bot_100": self.bot_100,
            "top_200": self.top_200,
            "mid_200": self.mid_200,
            "bot_200": self.bot_200
        }

        self.send_data(**data)
