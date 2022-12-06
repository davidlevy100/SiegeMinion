from string import Template

import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_controller import DataEventDispatcher
from data.events.current.activatable import L3Activatable


class PlayerRunesL3(L3Activatable):

    #External Properties
    player_map = kp.DictProperty({})
    sorted_players = kp.ListProperty([])

    available_players = kp.ListProperty([])

    #Preview Properties
    preview_title = kp.StringProperty("")

    preview_tricode = kp.StringProperty("")

    preview_player = kp.ObjectProperty(allownone=True)
    preview_player_name = kp.StringProperty("")

    preview_champion = kp.DictProperty()

    #Runes
    preview_primary_tree = kp.DictProperty()
    preview_secondary_tree = kp.DictProperty()

    preview_keystone = kp.DictProperty()

    preview_rune1 = kp.DictProperty()
    preview_rune2 = kp.DictProperty()
    preview_rune3 = kp.DictProperty()
    preview_rune4 = kp.DictProperty()
    preview_rune5 = kp.DictProperty()


    #Active Properties
    
    ##active_title inherited

    active_player_name = kp.StringProperty("")
    active_tricode = kp.StringProperty("")

    active_champion = kp.DictProperty()

    #Runes
    active_primary_tree = kp.DictProperty()
    active_secondary_tree = kp.DictProperty()

    active_keystone = kp.DictProperty()

    active_rune1 = kp.DictProperty()
    active_rune2 = kp.DictProperty()
    active_rune3 = kp.DictProperty()
    active_rune4 = kp.DictProperty()
    active_rune5 = kp.DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.overlay_players.bind(player_map=self.setter('player_map'))
        self.app.overlay_players.bind(sorted_players=self.setter('sorted_players'))

        #These variables help determine when this graphic is visible to the user
        self.graphic_type = "Lower 3rds"
        self.graphic_name = "Player Runes"


    def on_game_reset(self, *args):
        super().on_game_reset(*args)

        self.reset_preview()
        self.reset_active()

    
    def on_preview_player(self, *args):

        if self.preview_player is not None:

            raw_title = self.app.config.getdefault("User Game Data", "player_runes_l3_title", "")
            self.preview_title = Template(raw_title).safe_substitute(
                player=self.preview_player.name,
                PLAYER=self.preview_player.name.upper()
            )

            self.preview_tricode = self.preview_player.tricode

            self.preview_player_name = self.preview_player.name

            self.preview_champion = self.preview_player.pick_champion

            self.preview_primary_tree = self.preview_player.primary_tree
            self.preview_secondary_tree = self.preview_player.secondary_tree

            self.preview_keystone = self.preview_player.keystone

            self.preview_rune1 = self.preview_player.rune1
            self.preview_rune2 = self.preview_player.rune2
            self.preview_rune3 = self.preview_player.rune3
            self.preview_rune4 = self.preview_player.rune4
            self.preview_rune5 = self.preview_player.rune5

        else:

            self.preview_title = ""

            self.preview_tricode = ""

            self.preview_player_name = ""

            self.preview_champion = {}

            self.preview_primary_tree = {}
            self.preview_secondary_tree = {}

            self.preview_keystone = {}

            self.preview_rune1 = {}
            self.preview_rune2 = {}
            self.preview_rune3 = {}
            self.preview_rune4 = {}
            self.preview_rune5 = {}




    def on_sorted_players(self, *args):
        self.update_available_players()

        if len(self.available_players) > 0:
            self.select_player(self.available_players[0])


    def select_player(self, player_name, *args):

        if player_name in self.player_map:
            self.preview_player = self.player_map[player_name]


    def set_active(self, is_active, *args):

        if is_active:
            self.active_title = self.preview_title
            self.active_player_name = self.preview_player_name
            self.active_tricode = self.preview_tricode
            self.active_champion = self.preview_champion

            self.active_primary_tree = self.preview_primary_tree
            self.active_secondary_tree = self.preview_secondary_tree

            self.active_keystone = self.preview_keystone

            self.active_rune1 = self.preview_rune1
            self.active_rune2 = self.preview_rune2
            self.active_rune3 = self.preview_rune3
            self.active_rune4 = self.preview_rune4
            self.active_rune5 = self.preview_rune5

        else:

            self.reset_active()

        super().set_active(is_active)


    def reset_active(self, *args):
        self.active_title = ""
        self.active_player_name = ""
        self.active_tricode = ""
        self.active_champion = {}

        self.active_primary_tree = {}
        self.active_secondary_tree = {}

        self.active_keystone = {}

        self.active_rune1 = {}
        self.active_rune2 = {}
        self.active_rune3 = {}
        self.active_rune4 = {}
        self.active_rune5 = {}

    def reset_preview(self, *args):
        self.preview_player = None
        self.preview_title = ""
        self.preview_player_name = ""
        self.preview_tricode = ""

        self.preview_primary_tree = {}
        self.preview_secondary_tree = {}

        self.preview_keystone = {}

        self.preview_rune1 = {}
        self.preview_rune2 = {}
        self.preview_rune3 = {}
        self.preview_rune4 = {}
        self.preview_rune5 = {}

    def update_available_players(self, *args):
        self.available_players = [k for k,v in self.sorted_players]

    def update_properties(self, *args):
        pass
