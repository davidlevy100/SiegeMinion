import kivy.properties as kp
from kivy.logger import Logger

from data.vizrt.vizcrank.sender import VizcrankSender


class L3ItemBuildSender(VizcrankSender):

    tricode_left = kp.StringProperty()
    tricode_right = kp.StringProperty()

    viz_logo_left = kp.StringProperty()
    viz_logo_right = kp.StringProperty()

    #External Properties
    player_map = kp.DictProperty({})
    sorted_players = kp.ListProperty([])

    sorted_player_names = kp.ListProperty([])
    selected_player_name = kp.StringProperty("")

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
        self.sorted_player_names.clear()
        for player in self.sorted_players:
            self.sorted_player_names.append(player[0])

    def can_process(self, *args):
        return self.selected_player_name \
            and len(self.selected_player_name) > 0 \
            and self.selected_player_name in self.player_map
        
    def process_game_data(self, game_data, *args):
        if not self.can_process():
            return dict()
        
        selected_player = self.player_map[self.selected_player_name]

        #Color Bars
        self.safe_set_field(game_data, "0001", 0)
        self.safe_set_field(game_data, "0002", 0)

        #Number of Items
        item_count = len(selected_player.inventory.item_list)
        self.safe_set_field(game_data, "0003", str(item_count))
        
        #Header
        self.safe_set_field(game_data, "0050", selected_player.name) #TRI PLAYER AS CHAMPION??

        #Champ Image
        self.safe_set_field(game_data, "0090", selected_player.pick_champion["internal_name"])

        #Team Logo
        self.safe_set_field(game_data, "0100", selected_player.tricode)

        #Item Build
        self.safe_set_field(game_data, "0110", "ITEM BUILD")

        #Items
        item_fields = ["0121", "0122", "0123", "0124", "0125", "0126"]
        for idx, item in enumerate(selected_player.inventory.item_list):
            self.safe_set_field(game_data, item_fields[idx], item["internal_name"])

        return game_data  
