import kivy.properties as kp
from kivy.logger import Logger

from data.vizrt.vizcrank.sender import VizcrankSender


class ItemBuildL3Sender(VizcrankSender):

    tricode_left = kp.StringProperty()
    tricode_right = kp.StringProperty()

    viz_logo_left = kp.StringProperty()
    viz_logo_right = kp.StringProperty()

    #External Properties
    player_map = kp.DictProperty({})
    sorted_players = kp.ListProperty([])
    selected_player = kp.ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.game_data.bind(tricode_left=self.setter('tricode_left'))
        self.app.game_data.bind(tricode_right=self.setter('tricode_right'))

        self.viz_logo_left = self.app.viz_mutator.viz_logo_left
        self.app.viz_mutator.bind(viz_logo_left=self.setter('viz_logo_left'))

        self.viz_logo_right = self.app.viz_mutator.viz_logo_right
        self.app.viz_mutator.bind(viz_logo_right=self.setter('viz_logo_right'))

        self.app.overlay_players.bind(player_map=self.setter('player_map'))
        self.app.overlay_players.bind(sorted_players=self.setter('sorted_players'))

        #Config Keys
        self.section = "Item Build L3"


    def on_sorted_players(self, *args):

        if len(self.player_map) > 0:
            self.select_player(self.sorted_players[0][0])


    def select_player(self, player_name, *args):

        if player_name in self.player_map:
            self.selected_player = self.player_map[player_name]


    def can_process(self, *args):
        return self.selected_player is not None
        
    def process_game_data(self, game_data, *args):
        
        if self.selected_player is None:
            return dict()

        print(self.selected_player.inventory.item6)

        #Color Bars
        field = "0001"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = 0

        field = "0002"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = 0


        #Number of Items
        field = "0006"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = 6 #need to add code to count items

        
        #Header
        field = "0050"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = 0 #TRI PLAYER AS CHAMPION

        #Champ Image
        field = "0090"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = self.selected_player.pick_champion["internal_name"]

        #Team Logo
        field = "0100"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = "team Logo"

        #Item Build
        field = "0110"
        if self.has_field(field=field, fields=game_data["fields"], key="value"):
            game_data["fields"][field]["value"] = "ITEM BUILD"

        #Loop to fill out items


        


        return game_data  
