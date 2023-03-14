import kivy.properties as kp

from data.vizrt.vizcrank.sender import VizcrankSender
from data.esports.stats import convert_milliseconds_to_HMS_string
from data.esports.stats import format_number

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

    pause_started_event = kp.DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.live_data.bind(pause_started_event=self.setter('pause_started_event'))

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
        if len(self.pause_started_event) > 0 and "gameTime" in self.pause_started_event:
            # Turn Dots Off
            self.safe_set_field(game_data, "0001", "0")

            # Header
            self.safe_set_field(game_data, "0050", "Game Pause")

            # Game Time
            game_time_ms = self.pause_started_event["gameTime"]
            self.safe_set_field(game_data, "0060", convert_milliseconds_to_HMS_string(game_time_ms))

            # Blue Team Logo
            self.safe_set_field(game_data, "0100", self.app.viz_mutator.viz_logo_left)

            # Red Team Logo
            self.safe_set_field(game_data, "0200", self.app.viz_mutator.viz_logo_right)

            game_state_idx = self.app.livestats_history.get_history_index(game_time_ms)
            if game_state_idx is not None:
                game_state = self.app.livestats_history.stats_update_history.values()[game_state_idx]
                self.populate_game_state(game_data, game_state)

        return game_data
    
    def populate_game_state(self, game_data, game_state):
        # Blue Towers
        self.safe_set_field(game_data, "0121", str(game_state["towers"]["blue_turret_kills"]))

        # Red Towers
        self.safe_set_field(game_data, "0221", str(game_state["towers"]["red_turret_kills"]))

        # Team data
        blue_team = game_state["teams"][0]
        red_team = game_state["teams"][1]

        # Dragons
        blue_on_off_fields = ["0150", "0160", "0170", "0180"]
        blue_image_fields = ["0151", "0161", "0171", "0181"]
        red_on_off_fields = ["0250", "0260", "0270", "0280"]
        red_image_fields = ["0251", "0261", "0271", "0281"]

        blue_dragons = blue_team["dragons"]
        red_dragons = red_team["dragons"]
        for idx in range(4):
            blue_on_off_field = blue_on_off_fields[idx]
            blue_image_field = blue_image_fields[idx]
            has_blue_dragon = idx < len(blue_dragons)
            if has_blue_dragon:
                self.safe_set_field(game_data, blue_on_off_field, "1")
                self.safe_set_field(game_data, blue_image_field, self.get_dragon_name(blue_dragons[idx]))
            else:
                self.safe_set_field(game_data, blue_on_off_field, "0")
            
            red_on_off_field = red_on_off_fields[idx]
            red_image_field = red_image_fields[idx]
            has_red_dragon = idx < len(red_dragons)
            if has_red_dragon:
                self.safe_set_field(game_data, red_on_off_field, "1")
                self.safe_set_field(game_data, red_image_field, self.get_dragon_name(red_dragons[idx]))
            else:
                self.safe_set_field(game_data, red_on_off_field, "0")

        # Kills
        blue_kills_field = "0141"
        red_kills_field = "0241"
        if "championsKills" in blue_team and "championsKills" in red_team:
            self.safe_set_field(game_data, blue_kills_field, str(blue_team["championsKills"]))
            self.safe_set_field(game_data, red_kills_field, str(red_team["championsKills"]))
            
        # Gold
        blue_gold_field = "0131"
        red_gold_field = "0231"
        if "totalGold" in blue_team and "totalGold" in red_team:
            self.safe_set_field(game_data, blue_gold_field, format_number(blue_team["totalGold"]))
            self.safe_set_field(game_data, red_gold_field, format_number(red_team["totalGold"]))

    def get_dragon_name(self, dragon):
        return DRAGON_NAME_MAP[dragon] if dragon in DRAGON_NAME_MAP else "_Placeholder"
    
    def safe_set_field(self, game_data, field, value):
        """ helper function to verify the field is present and then set the value in it """
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = value
