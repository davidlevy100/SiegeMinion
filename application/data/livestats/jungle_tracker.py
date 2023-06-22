from math import sqrt
from sortedcontainers import SortedDict

import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher


COUNTERJUNGLE_START = 3*60000
COUNTERJUNGLE_END = 15*60000


class JungleTracker(DataEventDispatcher):

    latest_stats_update = kp.DictProperty()
    counter_jungle_stats = kp.ListProperty([0.0]*2)

    blue_counter, red_counter = 0, 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.latest_stats_update = self.app.live_data.latest_stats_update
        self.app.live_data.bind(latest_stats_update=self.setter('latest_stats_update'))


    def on_latest_stats_update(self, *args):
        
        if ("gameTime" in self.latest_stats_update and
            "participants" in self.latest_stats_update and
            len(self.latest_stats_update["participants"]) > 6
        ):
            
            game_time = self.latest_stats_update["gameTime"]
            
            if game_time < COUNTERJUNGLE_START:
                self.blue_counter, self.red_counter = 0, 0
                self.counter_jungle_stats = [0.0]*2

            elif COUNTERJUNGLE_START <= game_time <= COUNTERJUNGLE_END:

                blue_jungler = self.latest_stats_update["participants"][1]
                red_jungler = self.latest_stats_update["participants"][6]

                if self.isCounterJungling(blue_jungler, game_time):
                    self.blue_counter = self.blue_counter + 1

                if self.isCounterJungling(red_jungler, game_time):
                    self.red_counter = self.red_counter + 1

                timedelta = game_time - COUNTERJUNGLE_START

                blue_stat = (self.blue_counter * 1000)/timedelta
                red_stat = (self.red_counter * 1000)/timedelta

                self.counter_jungle_stats = [blue_stat, red_stat]

            else:

                timedelta = COUNTERJUNGLE_END - COUNTERJUNGLE_START

                blue_stat = (self.blue_counter * 1000)/timedelta
                red_stat = (self.red_counter * 1000)/timedelta

                self.counter_jungle_stats = [blue_stat, red_stat]


    def on_game_reset(self, *args):
        self.counter_jungle_stats = [0.0]*2
        self.blue_counter = 0
        self.red_counter = 0
    
    
    def isCounterJungling(self, jungler, time,) -> bool:

        ID, x, y = 0,0,0

        if not "participantID" in jungler:
            LogMessage = (f"could not get jungler ID at gametime: {time}")
            Logger.error(LogMessage)
            return False
        else:
            ID = jungler["participantID"]
        
        if not ("position" in jungler and
            "x" in jungler["position"] and
            "z" in jungler["position"]
        ):
            LogMessage = (f"could not get jungler position at gametime: {time}")
            Logger.error(LogMessage)
            return False
        else:
            x = jungler["position"]["x"]
            y = jungler["position"]["z"]


        #Top Lane?
        if x <= 2000 or y >= 13000:
            return False
        
        #Bot Lane?
        if x >= 13000 or y <= 2000:
            return False
        
        #Mid Lane?
        if ((x * .937 - 400) <= y) and (y <= (x * .937 + 1430)):
            return False

        #Blue Base?
        blueBaseDistance = sqrt((y - 300) ** 2 + (x - 300) ** 2)
        if blueBaseDistance <= 5250:
            return False
        
        #Red Base?
        redBaseDistance = sqrt((y - 14450) ** 2 + (x - 14450) ** 2)
        if redBaseDistance <= 5100:
            return False
        
        #Top Lane Test 2
        topLaneDistance = sqrt((y - 14000) ** 2 + (x - 500) ** 2)
        if topLaneDistance <= 3000:
            return False
        
        #Bot Lane Test 2
        botLaneDistance = sqrt((y - 500) ** 2 + (x - 14000) ** 2)
        if botLaneDistance <= 3000:
            return False

        #Baron Pit Test
        baronDistance = sqrt((y - 10396) ** 2 + (x - 5055) ** 2)
        if baronDistance < 850:
            return False
        
        #Dragon Pit Test
        dragDistance = sqrt((y - 4524) ** 2 + (x - 9850) ** 2)
        if dragDistance < 700:
            return False
        
        #Top Brush Test
        topBrushDistance = sqrt((y - 8159) ** 2 + (x - 5180) ** 2)
        if topBrushDistance < 415:
            return False
        
        #Initial Jungle Test
        region = ""
        if (x * .937 - 400) <= y:
            region = "Top Jungle"
        elif y <= (x * .937 + 1430):
            region = "Bot Jungle"

        #River Test
        if (region == "Top Jungle" or region == "Bot Jungle") and (
            (y < (x * -.83 + 15000)) and (y > (x * -.85 + 12600))
        ):
            #river, return False
            return False
        
        #Enemy Jungle Test
        if region == "Top Jungle" or region == "Bot Jungle":
            
            #In Red Jungle?
            if y >= (x * -.85 + 13500):
                #Blue Jungler in Red Jungle?
                if ID == 1:
                    return True
                else:
                    return False
            
            #In Blue Jungle
            else:
                #Red Jungler in Blue Jungle?
                if ID == 6:
                    return True
                else:
                    return False

        return False
    