import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher
from data.esports.stats import convert_milliseconds_to_HMS_string


class ChampionKillsDispatcher(DataEventDispatcher):

    champion_kill_event = kp.DictProperty()
    champion_kills = kp.ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.live_data.bind(champion_kill_event=self.setter('champion_kill_event'))


    def on_game_reset(self, *args):
        self.champion_kills.clear()
        Logger.info("Champion kills: has been reset")


    def on_champion_kill_event(self, *args):
        if ("gameTime" in self.champion_kill_event and
            "assistants" in self.champion_kill_event and
            "killer" in self.champion_kill_event and
            "victim" in self.champion_kill_event):

            gametime = convert_milliseconds_to_HMS_string(self.champion_kill_event["gameTime"])
            assistants = self.champion_kill_event["assistants"]
            killer = self.champion_kill_event["killer"]
            victim = self.champion_kill_event["victim"]

            LogMessage = (f"Champion Kill: participant {killer} killed participant {victim} at gametime: {gametime}")
            Logger.info(LogMessage)

            data = {
                "gameTime": gametime,
                "killer": killer,
                "victim": victim,
                "assistants": assistants
            }
            self.champion_kills.append(data)
