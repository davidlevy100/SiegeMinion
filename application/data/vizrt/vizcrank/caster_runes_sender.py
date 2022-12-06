import kivy.properties as kp
from kivy.logger import Logger

from data.vizrt.vizcrank.sender import VizcrankSender


FIELD_PREFIXES = {
    0: 100,
    1: 200,
    2: 300,
    3: 400,
    4: 500, 
    5: 120,
    6: 220,
    7: 320,
    8: 420,
    9: 520
}


class CasterRunesSender(VizcrankSender):

    tricode_left = kp.StringProperty()
    tricode_right = kp.StringProperty()

    viz_logo_left = kp.StringProperty()
    viz_logo_right = kp.StringProperty()

    game_info_event = kp.DictProperty({})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.live_data.bind(game_info_event=self.setter('game_info_event'))
        self.app.game_data.bind(tricode_left=self.setter('tricode_left'))
        self.app.game_data.bind(tricode_right=self.setter('tricode_right'))

        self.viz_logo_left = self.app.viz_mutator.viz_logo_left
        self.app.viz_mutator.bind(viz_logo_left=self.setter('viz_logo_left'))

        self.viz_logo_right = self.app.viz_mutator.viz_logo_right
        self.app.viz_mutator.bind(viz_logo_right=self.setter('viz_logo_right'))

        #Config Keys
        self.section = "Caster Runes"

    
    def on_game_info_event(self, *args):

        if not self.can_process():
            return

        if not (self.auto_slack or self.auto_trio):
            return

        if self.auto_slack:
            self.send_to_slack()

        if self.auto_trio:
            self.send_to_trio()


    def can_process(self, *args):

        if len(self.game_info_event) == 0:
            return False

        else:
            return True


    def process_game_data(self, game_data, *args):

        if "participants" not in self.game_info_event:
            return

        #Left Team Logo
        field = "0010"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = self.viz_logo_left

        #Left Team Text Name
        field = "0011"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):

            team_name = self.app.config.get("Team Tricodes", self.tricode_left.lower(), fallback=self.tricode_left)
            game_data["fields"][field]["value"] = team_name.upper()


        #Right Team Logo
        field = "0020"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = self.viz_logo_right

        #Right Team Text Name
        field = "0021"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):

            team_name = self.app.config.get("Team Tricodes", self.tricode_right.lower(), fallback=self.tricode_right)
            game_data["fields"][field]["value"] = team_name.upper()


        for index, this_participant in enumerate(self.game_info_event["participants"]):

            try:

                offset = FIELD_PREFIXES[index]

                # Main Path Viz Name
                main_path = self.app.data_dragon.get_asset("rune", this_participant["perks"][0]["perkStyle"])
                if main_path is not None:
                    
                    field = f"0{offset+0}"
                    if self.has_field(field=field, fields=game_data["fields"], key="value"):
                        game_data["fields"][field]["value"] = main_path["long_name"]


                # Keystone Viz Name & External Name
                keystone = self.app.data_dragon.get_asset("rune", this_participant["keystoneID"])
                if keystone is not None:
                    field = f"0{offset+1}"
                    if self.has_field(field=field, fields=game_data["fields"], key="value"):
                        game_data["fields"][field]["value"] = keystone["long_name"]

                    field = f"0{offset+2}"
                    if self.has_field(field=field, fields=game_data["fields"], key="value"):
                        game_data["fields"][field]["value"] = keystone["external_name"]


                # Rune 1 Viz Name & External Name
                rune1 = self.app.data_dragon.get_asset("rune", this_participant["perks"][0]["perkIds"][1])
                if rune1 is not None:
                    field = f"0{offset+3}"
                    if self.has_field(field=field, fields=game_data["fields"], key="value"):
                        game_data["fields"][field]["value"] = rune1["long_name"]

                    field = f"0{offset+4}"
                    if self.has_field(field=field, fields=game_data["fields"], key="value"):
                        game_data["fields"][field]["value"] = rune1["external_name"]


                # Rune 2 Viz Name & External Name
                rune2 = self.app.data_dragon.get_asset("rune", this_participant["perks"][0]["perkIds"][2])
                if rune2 is not None:
                    field = f"0{offset+5}"
                    if self.has_field(field=field, fields=game_data["fields"], key="value"):
                        game_data["fields"][field]["value"] = rune2["long_name"]

                    field = f"0{offset+6}"
                    if self.has_field(field=field, fields=game_data["fields"], key="value"):
                        game_data["fields"][field]["value"] = rune2["external_name"]


                # Rune 3 Viz Name & External Name
                rune3 = self.app.data_dragon.get_asset("rune", this_participant["perks"][0]["perkIds"][3])
                if rune3 is not None:
                    field = f"0{offset+7}"
                    if self.has_field(field=field, fields=game_data["fields"], key="value"):
                        game_data["fields"][field]["value"] = rune3["long_name"]

                    field = f"0{offset+8}"
                    if self.has_field(field=field, fields=game_data["fields"], key="value"):
                        game_data["fields"][field]["value"] = rune3["external_name"]


                # Secondary Path Viz Name
                secondary_path = self.app.data_dragon.get_asset("rune", this_participant["perks"][0]["perkSubStyle"])
                if secondary_path is not None:
                    field = f"0{offset+10}"
                    if self.has_field(field=field, fields=game_data["fields"], key="value"):
                        game_data["fields"][field]["value"] = secondary_path["long_name"]


                # Rune 4 Viz Name & External Name
                rune4 = self.app.data_dragon.get_asset("rune", this_participant["perks"][0]["perkIds"][4])
                if rune4 is not None:
                    field = f"0{offset+11}"
                    if self.has_field(field=field, fields=game_data["fields"], key="value"):
                        game_data["fields"][field]["value"] = rune4["long_name"]
                    
                    field = f"0{offset+12}"
                    if self.has_field(field=field, fields=game_data["fields"], key="value"):
                        game_data["fields"][field]["value"] = rune4["external_name"]

                # Rune 5 Viz Name & External Name
                rune5 = self.app.data_dragon.get_asset("rune", this_participant["perks"][0]["perkIds"][5])
                if rune5 is not None:
                    field = f"0{offset+13}"
                    if self.has_field(field=field, fields=game_data["fields"], key="value"):
                        game_data["fields"][field]["value"] = rune5["long_name"]
                    
                    field = f"0{offset+14}"
                    if self.has_field(field=field, fields=game_data["fields"], key="value"):
                        game_data["fields"][field]["value"] = rune5["external_name"]

                # Champion Internal Name
                if "championName" in this_participant:
                    champion = self.app.data_dragon.get_asset("champion", this_participant["championName"])
                    if champion is not None:
                        field = f"0{offset+15}"
                        if self.has_field(field=field, fields=game_data["fields"], key="value"):
                            game_data["fields"][f"0{offset+15}"]["value"] = champion["internal_name"]

                # Player Name
                if "summonerName" in this_participant:
                    name = this_participant["summonerName"]
                    name_array = this_participant["summonerName"].split(" ")

                    if len(name_array) > 1:
                        name = " ".join(name_array[1:])

                    field = f"0{offset+16}"
                    if self.has_field(field=field, fields=game_data["fields"], key="value"):
                        game_data["fields"][field]["value"] = name

            except Exception as e:
                Logger.exception(f"Error: {e}")
                return

        return game_data  
