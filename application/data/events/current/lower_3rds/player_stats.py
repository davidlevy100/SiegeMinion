from string import Template

import kivy.properties as kp
from kivy.logger import Logger


from data.events.data_controller import DataEventDispatcher
from data.events.current.activatable import L3Activatable

from data.esports.stats import STRING_STAT_MAP
from data.esports.stats import string_KDA, string_CS, string_CSD, string_GD, string_DMG, string_GOLD, string_DMG_D, string_LEVEL, string_XPD, string_VISION, string_default

ALL_STATS = sorted(STRING_STAT_MAP.keys())[1:]

DEFAULT_CATS = ["GOLD", "GD", "CSD", "DMG"]


class PlayerStatsL3(L3Activatable):

    #External Properties
    player_map = kp.DictProperty({})
    sorted_players = kp.ListProperty([])
    current_stats_update = kp.DictProperty()

    available_players = kp.ListProperty([])
    available_categories = kp.ListProperty(ALL_STATS)

    #Preview Properties
    preview_title = kp.StringProperty("")

    preview_tricode = kp.StringProperty("")

    preview_player = kp.ObjectProperty(allownone=True)

    preview_participant_ID = kp.NumericProperty(0)
    preview_opponent_ID = kp.NumericProperty(0)

    preview_player_name = kp.StringProperty("")

    preview_champion = kp.DictProperty()

    preview_cat1 = kp.StringProperty("")
    preview_cat2 = kp.StringProperty("")
    preview_cat3 = kp.StringProperty("")
    preview_cat4 = kp.StringProperty("")

    preview_stat1 = kp.StringProperty("")
    preview_stat2 = kp.StringProperty("")
    preview_stat3 = kp.StringProperty("")
    preview_stat4 = kp.StringProperty("")

    
    #Active Properties
    
    ##active_title inherited

    active_player_name = kp.StringProperty("")

    active_tricode = kp.StringProperty("")

    active_participant_ID = kp.NumericProperty(0)
    active_opponent_ID = kp.NumericProperty(0)

    active_champion = kp.DictProperty()

    active_cat1 = kp.StringProperty("")
    active_cat2 = kp.StringProperty("")
    active_cat3 = kp.StringProperty("")
    active_cat4 = kp.StringProperty("")

    active_stat1 = kp.StringProperty("")
    active_stat2 = kp.StringProperty("")
    active_stat3 = kp.StringProperty("")
    active_stat4 = kp.StringProperty("")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.livestats_history.bind(
            current_stats_update=self.setter('current_stats_update')
        )

        self.app.overlay_players.bind(player_map=self.setter('player_map'))
        self.app.overlay_players.bind(sorted_players=self.setter('sorted_players'))

        #These variables help determine when this graphic is visible to the user
        self.graphic_type = "Lower 3rds"
        self.graphic_name = "Player Stats"


    def on_current_stats_update(self, *args):

        if (self.visible or 
            self.active
        ):
            self.update_properties()


    def on_game_reset(self, *args):
        super().on_game_reset(*args)

        self.reset_categories()
        self.reset_active()
        self.reset_preview()


    def on_preview_player(self, *args):

        if self.preview_player is not None:

            self.preview_participant_ID = self.preview_player.participant_ID

            if self.preview_participant_ID < 6:
                self.preview_opponent_ID = self.preview_participant_ID + 5

            else:
                self.preview_opponent_ID = self.preview_participant_ID - 5

            self.preview_player_name = self.preview_player.name
            self.preview_champion = self.preview_player.pick_champion
            self.preview_tricode = self.preview_player.tricode

        else:

            self.preview_participant_ID = 0
            self.preview_opponent_ID = 0
            self.preview_player_name = ""
            self.preview_champion = {}
            self.preview_tricode = ""


    def on_sorted_players(self, *args):
        self.update_available_players()

        if len(self.available_players) > 0:
            self.select_player(self.available_players[0])


    def get_participant(self, participants, id, *args):

        result = None

        for this_participant in participants:
            if ("participantID" in this_participant and
                this_participant["participantID"] == id
            ):
                return this_participant

        return result


    def get_stats(self, stat_type, category, index, player, opponent, *args):

        new_value = STRING_STAT_MAP[category](player, opponent)

        stat_name = f"{stat_type}_stat{index}"

        if stat_name in self.properties():
            stat_prop = self.property(stat_name)
            stat_prop.set(self, str(new_value))


    def select_category(self, cat_name, index, *args):

        cat_prop_name = f"preview_cat{index}"

        if (cat_prop_name in self.properties() and
            cat_name in STRING_STAT_MAP
        ):
            cat_property = self.property(cat_prop_name)
            cat_property.set(self, cat_name)
            self.update_available_categories()


    def select_player(self, player_name, *args):

        if player_name in self.player_map:
            self.preview_player = self.player_map[player_name]

        if self.preview_player is not None:

            raw_title = self.app.config.getdefault("User Game Data", "player_stats_l3_title", "")

            self.preview_title = Template(raw_title).safe_substitute(
                player=self.preview_player.name,
                PLAYER=self.preview_player.name.upper()
            )
    
    def set_active(self, is_active, *args):

        if is_active:
            self.active_title = self.preview_title
            
            self.active_player_name = self.preview_player_name

            self.active_tricode = self.preview_tricode

            self.active_participant_ID = self.preview_participant_ID
            self.active_opponent_ID = self.preview_opponent_ID

            self.active_champion = self.preview_champion

            self.active_cat1 = self.preview_cat1
            self.active_cat2 = self.preview_cat2
            self.active_cat3 = self.preview_cat3
            self.active_cat4 = self.preview_cat4

            self.active_stat1 = self.preview_stat1
            self.active_stat2 = self.preview_stat2
            self.active_stat3 = self.preview_stat3
            self.active_stat4 = self.preview_stat4

        else:

            self.reset_active()

        super().set_active(is_active)


    def reset_active(self, *args):

        self.active_title = ""
        
        self.active_player_name = ""
        self.active_tricode = ""

        self.active_participant_ID = 0
        self.active_opponent_ID = 0
        self.active_champion = {}

        self.active_cat1 = ""
        self.active_cat2 = ""
        self.active_cat3 = ""
        self.active_cat4 = ""

        self.active_stat1 = ""
        self.active_stat2 = ""
        self.active_stat3 = ""
        self.active_stat4 = ""


    def reset_categories(self, *args):

        for index, this_cat in enumerate(DEFAULT_CATS, 1):
            self.select_category(this_cat, index)


    def reset_preview(self, *args):

        self.preview_title = ""

        self.preview_player = None
        self.preview_tricode = ""

        self.preview_participant_ID = 0
        self.preview_opponent_ID = 0

        self.preview_player_name = ""

        self.preview_champion = {}

        self.preview_stat1 = ""
        self.preview_stat2 = ""
        self.preview_stat3 = ""
        self.preview_stat4 = ""


    def update_active(self, *args):

        if "participants" in self.current_stats_update:
            left_participant = self.get_participant(
                self.current_stats_update["participants"],
                self.active_participant_ID
            )

            if left_participant is None:
                return

            right_participant = self.get_participant(
                self.current_stats_update["participants"],
                self.active_opponent_ID
            )

            if right_participant is None:
                return

            for index, this_category in enumerate([
                self.active_cat1,
                self.active_cat2,
                self.active_cat3,
                self.active_cat4
            ], 1):

                self.get_stats("active", this_category, index, left_participant, right_participant)


    def update_available_players(self, *args):
        self.available_players = [k for k,v in self.sorted_players]

    def update_available_categories(self, *args):

        used_stats = []

        used_stats.append(self.preview_cat1)
        used_stats.append(self.preview_cat2)
        used_stats.append(self.preview_cat3)
        used_stats.append(self.preview_cat4)

        self.available_categories = [x for x in ALL_STATS if x not in used_stats]


    def update_preview(self, *args):

        if "participants" in self.current_stats_update:

            left_participant = self.get_participant(
                self.current_stats_update["participants"],
                self.preview_participant_ID
            )

            if left_participant is None:
                return

            right_participant = self.get_participant(
                self.current_stats_update["participants"],
                self.preview_opponent_ID
            )

            if right_participant is None:
                return

            for index, this_category in enumerate([
                self.preview_cat1,
                self.preview_cat2,
                self.preview_cat3,
                self.preview_cat4
            ], 1):

                self.get_stats("preview", this_category, index, left_participant, right_participant)


    def update_properties(self, *args):

        if self.visible:
            self.update_preview()

        if self.active:
            self.update_active()
