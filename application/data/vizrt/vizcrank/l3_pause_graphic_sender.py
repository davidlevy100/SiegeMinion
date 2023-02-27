import kivy.properties as kp

from data.vizrt.vizcrank.sender import VizcrankSender
from data.esports.stats import convert_milliseconds_to_HMS_string

# TODO where would be a good place to store this information?
DRAGON_NAME_MAP = {
    "air": "Drake_Cloud",
    "fire": "Drake_Infernal",
    "earth": "Drake_Mountain",
    "water": "Drake_Ocean",
    "chemtech": "Drake_Chemtech",
    "hextech": "Drake_Hextech"
}


class L3PauseGraphicSender(VizcrankSender):
    viz_logo_blue = kp.StringProperty()
    viz_logo_red = kp.StringProperty()

    latest_stats_update = kp.DictProperty()
    pause_started_event = kp.DictProperty({})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.live_data.bind(pause_started_event=self.setter('pause_started_event'))
        self.app.live_data.bind(latest_stats_update=self.setter('latest_stats_update'))

        self.viz_logo_blue = self.app.viz_mutator.viz_logo_left
        self.app.viz_mutator.bind(viz_logo_left=self.setter('viz_logo_blue'))

        self.viz_logo_red = self.app.viz_mutator.viz_logo_right
        self.app.viz_mutator.bind(viz_logo_right=self.setter('viz_logo_red'))

        # Config Keys
        self.section = "L3 Pause Graphic"

    def on_pause_started_event(self, *args):
        if not self.can_process():
            return

        if not (self.auto_slack or self.auto_trio):
            return

        if self.auto_slack:
            self.send_to_slack()

        if self.auto_trio:
            self.send_to_trio()

    def can_process(self, *args):
        if len(self.pause_started_event) == 0:
            return False

        else:
            return True

    def process_game_data(self, game_data, *args):
        # Turn Dots Off
        self.safe_set_field(game_data, "0001", 0)

        # Header
        self.safe_set_field(game_data, "0050", "Game Pause")

        # Game Time
        game_time = 0
        formatted_game_time = ""
        if "gameTime" in self.pause_started_event:
            game_time = self.pause_started_event["gameTime"]
            formatted_game_time = convert_milliseconds_to_HMS_string(game_time)
        self.safe_set_field(game_data, "0060", formatted_game_time)

        # Blue Team Logo
        self.safe_set_field(game_data, "0100", self.viz_logo_blue)

        # Red Team Logo
        self.safe_set_field(game_data, "0200", self.viz_logo_red)

        # Blue Towers
        self.safe_set_field(game_data, "0121", self.app.livestats_history.towers.blue_turret_kill_quantity)

        # Red Towers
        self.safe_set_field(game_data, "0221", self.app.livestats_history.towers.red_turret_kill_quantity)

        # Gold
        gold = self.app.gold_tracker.get_gold_at_game_time(game_time)

        # Blue gold
        self.safe_set_field(game_data, "0221", gold["blue_gold"])

        # Red Gold
        self.safe_set_field(game_data, "0231", gold["red_gold"])

        # Team data
        # TODO this may be wrong because latest stats update probably doesn't correlate to pause game time
        if len(self.latest_stats_update["teams"]) == 2:
            blue_team = self.latest_stats_update["teams"][0]
            red_team = self.latest_stats_update["teams"][1]

            # Kills
            blue_field = "0141"
            red_field = "0241"

            if "championKills" in blue_team:
                self.safe_set_field(game_data, blue_field, blue_team["championKills"])

            if "championKills" in red_team:
                self.safe_set_field(game_data, red_field, red_team["championKills"])

            # Dragons
            blue_dragons = []
            red_dragons = []
            # copied from post_game_breakdown_sender
            # confused where it comes from because I don't see a dragons array in the stats_update "teams" section
            for dragon in blue_team["dragons"]:
                blue_dragons.append(DRAGON_NAME_MAP.get(dragon, "_Placeholder"))

            for dragon in red_team["dragons"]:
                red_dragons.append(DRAGON_NAME_MAP.get(dragon, "_Placeholder"))

            # Blue Dragons
            blue_on_off_fields = ["0150", "0160", "0170", "0180"]
            blue_image_fields = ["0151", "0161", "0171", "0181"]
            for idx in range(4):
                on_off_field = blue_on_off_fields[idx]
                image_field = blue_image_fields[idx]
                has_dragon = idx < len(blue_dragons)
                self.safe_set_field(game_data, on_off_field, 1 if has_dragon else 0)
                self.safe_set_field(game_data, image_field, blue_dragons[idx] if has_dragon else "_Placeholder")

            # Red Dragons
            red_on_off_fields = ["0250", "0260", "0270", "0280"]
            red_image_fields = ["0251", "0261", "0271", "0281"]
            for idx in range(4):
                on_off_field = red_on_off_fields[idx]
                image_field = red_image_fields[idx]
                has_dragon = idx < len(red_dragons)
                self.safe_set_field(game_data, on_off_field, 1 if has_dragon else 0)
                self.safe_set_field(game_data, image_field, red_dragons[idx] if has_dragon else "_Placeholder")

        return game_data

    def safe_set_field(self, game_data, field, value):
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = value
