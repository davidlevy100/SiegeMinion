from string import Template

import kivy.properties as kp
from kivy.logger import Logger

from data.vizrt.vizcrank.sender import VizcrankSender

PICK_FIELDS = ["0111", "0121", "0131", "0141", "0151", "0211", "0221", "0231", "0241", "0251"]


class TeamPickOrderSender(VizcrankSender):

    tricode_left = kp.StringProperty()
    tricode_right = kp.StringProperty()

    viz_logo_left = kp.StringProperty()
    viz_logo_right = kp.StringProperty()

    champ_select_event = kp.DictProperty()
    game_info_event = kp.DictProperty({})

    title = kp.ConfigParserProperty(
        "",
        "Team Pick Order",
        "title",
        "app",
        val_type=str
    )

    pick_champion1 = kp.DictProperty()
    pick_champion2 = kp.DictProperty()
    pick_champion3 = kp.DictProperty()
    pick_champion4 = kp.DictProperty()
    pick_champion5 = kp.DictProperty()
    pick_champion6 = kp.DictProperty()
    pick_champion7 = kp.DictProperty()
    pick_champion8 = kp.DictProperty()
    pick_champion9 = kp.DictProperty()
    pick_champion10 = kp.DictProperty()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.live_data.bind(game_info_event=self.setter('game_info_event'))
        self.app.live_data.bind(champ_select_event=self.setter('champ_select_event'))
        self.app.game_data.bind(tricode_left=self.setter('tricode_left'))
        self.app.game_data.bind(tricode_right=self.setter('tricode_right'))

        self.viz_logo_left = self.app.viz_mutator.viz_logo_left
        self.app.viz_mutator.bind(viz_logo_left=self.setter('viz_logo_left'))

        self.viz_logo_right = self.app.viz_mutator.viz_logo_right
        self.app.viz_mutator.bind(viz_logo_right=self.setter('viz_logo_right'))

        self.app.overlay_players.player1.bind(pick_champion=self.setter('pick_champion1'))
        self.app.overlay_players.player2.bind(pick_champion=self.setter('pick_champion2'))
        self.app.overlay_players.player3.bind(pick_champion=self.setter('pick_champion3'))
        self.app.overlay_players.player4.bind(pick_champion=self.setter('pick_champion4'))
        self.app.overlay_players.player5.bind(pick_champion=self.setter('pick_champion5'))
        self.app.overlay_players.player6.bind(pick_champion=self.setter('pick_champion6'))
        self.app.overlay_players.player7.bind(pick_champion=self.setter('pick_champion7'))
        self.app.overlay_players.player8.bind(pick_champion=self.setter('pick_champion8'))
        self.app.overlay_players.player9.bind(pick_champion=self.setter('pick_champion9'))
        self.app.overlay_players.player10.bind(pick_champion=self.setter('pick_champion10'))

        #Config Keys
        self.section = "Team Pick Order"


    def can_process(self, *args):

        if len(self.game_info_event) == 0:
            return False

        else:
            return True

    
    def on_game_info_event(self, *args):

        if not self.can_process():
            return

        if not (self.auto_slack or self.auto_trio):
            return

        if self.auto_slack:
            self.send_to_slack()

        if self.auto_trio:
            self.send_to_trio()


    def process_game_data(self, game_data, *args):

        # Header
        field = "0050"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            
            try:
                new_title = Template(self.title).safe_substitute(
                    left_tricode=self.tricode_left, 
                    right_tricode=self.tricode_right
                )

            except Exception as e:
                Logger.exception(e)
                new_title = self.title

            game_data["fields"][field]["value"] = new_title

        #Blue Team Logo
        field = "0100"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = self.viz_logo_left

        #Blue Team Tricode
        field = "0101"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = self.tricode_left


        
        #Red Team Logo
        field = "0200"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = self.viz_logo_right

        #Red Team Logo
        field = "0201"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = self.tricode_right


        #Picks - Blue 0111 - 0151 / Red 0211 - 0251
        for index, field in enumerate(PICK_FIELDS, 1):

            # Champion Internal Name
            this_pick_champion = self.property(f'pick_champion{index}')
            champion = this_pick_champion.get(self)

            if ("internal_name" in champion and
                self.has_field(field=field, fields=game_data["fields"], key="value")
            ):
                game_data["fields"][field]["value"] = champion["internal_name"]


        # Bans - Blue 0171-0175 / Red 0271 - 0275
        if (len(self.champ_select_event) > 0 and
            "bannedChampions" in self.champ_select_event
        ):

            try:

                # Bans - Blue 0171-0175
                blue_ban_ids = [x["championID"] for x in self.champ_select_event["bannedChampions"] if x["teamID"] == 100]

                blue_bans = ["_Placeholder"] * 5
                
                for index, this_ban_id in enumerate(blue_ban_ids):
                    champion = self.app.data_dragon.get_asset("champion", f"{this_ban_id}")
                    if champion is not None:
                        blue_bans[index] = champion["internal_name"]

                for index, this_ban in enumerate(blue_bans, 171):
                    field = f"0{index}"
                    if self.has_field(field=field, fields=game_data["fields"], key="value"):
                        game_data["fields"][field]["value"] = this_ban


                # Bans - Red 0271 - 0275
                red_ban_ids = [x["championID"] for x in self.champ_select_event["bannedChampions"] if x["teamID"] == 200]

                red_bans = ["_Placeholder"] * 5

                for index, this_ban_id in enumerate(red_ban_ids):
                    champion = self.app.data_dragon.get_asset("champion", f"{this_ban_id}")
                    if champion is not None:
                        red_bans[index] = champion["internal_name"]

                for index, this_ban in enumerate(red_bans, 271):
                    field = f"0{index}"
                    if self.has_field(field=field, fields=game_data["fields"], key="value"):
                        game_data["fields"][field]["value"] = this_ban


            except Exception as e:
                Logger.exception(f"Error: {e}")

        return game_data
