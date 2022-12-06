from string import Template

import kivy.properties as kp
from kivy.logger import Logger


from data.events.data_controller import DataEventDispatcher
from data.events.current.activatable import L3Activatable

from data.esports.stats import STRING_STAT_MAP
from data.esports.stats import string_KDA, string_CS, string_CSD, string_GD, string_DMG, string_GOLD, string_DMG_D, string_LEVEL, string_XPD, string_VISION, string_default

ALL_STATS = sorted(STRING_STAT_MAP.keys())[1:]

DEFAULT_MATCHUP_CATS = ["K/D/A", "GOLD", "CS", "DMG"]


class PlayerMatchupL3(L3Activatable):

    #External Properties
    player_map = kp.DictProperty({})
    sorted_players = kp.ListProperty([])
    current_stats_update = kp.DictProperty()

    available_left_players = kp.ListProperty([])
    available_right_players = kp.ListProperty([])
    available_categories = kp.ListProperty(ALL_STATS)

    #Preview Properties
    preview_title = kp.StringProperty("")

    tricode_left = kp.StringProperty("")
    tricode_right = kp.StringProperty("")

    preview_left_player = kp.ObjectProperty(allownone=True)
    preview_right_player = kp.ObjectProperty(allownone=True)

    preview_left_participant_ID = kp.NumericProperty(0)
    preview_right_participant_ID = kp.NumericProperty(0)

    preview_left_player_name = kp.StringProperty("")
    preview_right_player_name = kp.StringProperty("")

    preview_left_champion = kp.DictProperty()
    preview_right_champion = kp.DictProperty()

    preview_cat1 = kp.StringProperty("")
    preview_cat2 = kp.StringProperty("")
    preview_cat3 = kp.StringProperty("")
    preview_cat4 = kp.StringProperty("")

    preview_left_stat1 = kp.StringProperty("")
    preview_left_stat2 = kp.StringProperty("")
    preview_left_stat3 = kp.StringProperty("")
    preview_left_stat4 = kp.StringProperty("")

    preview_right_stat1 = kp.StringProperty("")
    preview_right_stat2 = kp.StringProperty("")
    preview_right_stat3 = kp.StringProperty("")
    preview_right_stat4 = kp.StringProperty("")

    
    #Active Properties
    
    ##active_title inherited

    active_left_player_name = kp.StringProperty("")
    active_right_player_name = kp.StringProperty("")

    active_left_participant_ID = kp.NumericProperty(0)
    active_right_participant_ID = kp.NumericProperty(0)

    active_left_champion = kp.DictProperty()
    active_right_champion = kp.DictProperty()

    active_cat1 = kp.StringProperty("")
    active_cat2 = kp.StringProperty("")
    active_cat3 = kp.StringProperty("")
    active_cat4 = kp.StringProperty("")

    active_left_stat1 = kp.StringProperty("")
    active_left_stat2 = kp.StringProperty("")
    active_left_stat3 = kp.StringProperty("")
    active_left_stat4 = kp.StringProperty("")

    active_right_stat1 = kp.StringProperty("")
    active_right_stat2 = kp.StringProperty("")
    active_right_stat3 = kp.StringProperty("")
    active_right_stat4 = kp.StringProperty("")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.livestats_history.bind(
            current_stats_update=self.setter('current_stats_update')
        )

        self.app.overlay_players.bind(player_map=self.setter('player_map'))
        self.app.overlay_players.bind(sorted_players=self.setter('sorted_players'))

        #These variables help determine when this graphic is visible to the user
        self.graphic_type = "Lower 3rds"
        self.graphic_name = "Player Matchup"


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


    def on_preview_left_player(self, *args):

        if self.preview_left_player is not None:

            self.preview_left_participant_ID = self.preview_left_player.participant_ID
            self.preview_left_player_name = self.preview_left_player.name
            self.preview_left_champion = self.preview_left_player.pick_champion

        else:

            self.preview_left_participant_ID = 0
            self.preview_left_player_name = ""
            self.preview_left_champion = {}


    def on_preview_right_player(self, *args):

        if self.preview_right_player is not None:

            self.preview_right_participant_ID = self.preview_right_player.participant_ID
            self.preview_right_player_name = self.preview_right_player.name
            self.preview_right_champion = self.preview_right_player.pick_champion

        else:

            self.preview_right_participant_ID = 0
            self.preview_right_player_name = ""
            self.preview_right_champion = {}


    def on_sorted_players(self, *args):
        self.update_available_players()

        if len(self.available_left_players) > 0:
            self.select_player(self.available_left_players[0])


    def get_participant(self, participants, id, *args):

        result = None

        for this_participant in participants:
            if ("participantID" in this_participant and
                this_participant["participantID"] == id
            ):
                return this_participant

        return result


    def get_stats(self, stat_type, side, category, index, player, opponent, *args):

        new_value = STRING_STAT_MAP[category](player, opponent)

        stat_name = f"{stat_type}_{side}_stat{index}"

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
            new_player = self.player_map[player_name]

            if new_player.participant_ID < 6:
                self.preview_left_player = new_player
                new_right_player = self.app.overlay_players.find_player_by_id(new_player.participant_ID + 5)

                if new_right_player is not None:
                    self.preview_right_player = new_right_player

            else:
                self.preview_right_player = new_player

        if (self.preview_left_player is not None and
            self.preview_right_player is not None
        ):

            raw_title = self.app.config.getdefault("User Game Data", "player_matchup_l3_title", "")

            self.preview_title = Template(raw_title).safe_substitute(
                left_player=self.preview_left_player.name,
                right_player=self.preview_right_player.name,
                LEFT_PLAYER=self.preview_left_player.name.upper(),
                RIGHT_PLAYER=self.preview_right_player.name.upper()
            )

    
    def set_active(self, is_active, *args):

        if is_active:
            self.active_title = self.preview_title
            
            self.active_left_player_name = self.preview_left_player_name
            self.active_right_player_name = self.preview_right_player_name

            self.active_left_participant_ID = self.preview_left_participant_ID
            self.active_right_participant_ID = self.preview_right_participant_ID

            self.active_left_champion = self.preview_left_champion
            self.active_right_champion = self.preview_right_champion

            self.active_cat1 = self.preview_cat1
            self.active_cat2 = self.preview_cat2
            self.active_cat3 = self.preview_cat3
            self.active_cat4 = self.preview_cat4

            self.active_left_stat1 = self.preview_left_stat1
            self.active_left_stat2 = self.preview_left_stat2
            self.active_left_stat3 = self.preview_left_stat3
            self.active_left_stat4 = self.preview_left_stat4

            self.active_right_stat1 = self.preview_right_stat1
            self.active_right_stat2 = self.preview_right_stat2
            self.active_right_stat3 = self.preview_right_stat3
            self.active_right_stat4 = self.preview_right_stat4

        else:

            self.reset_active()

        super().set_active(is_active)


    def reset_active(self, *args):

        self.active_title = ""
        
        self.active_left_player_name = ""
        self.active_right_player_name = ""

        self.active_left_participant_ID = 0
        self.active_right_participant_ID = 0

        self.active_left_champion = {}
        self.active_right_champion = {}

        self.active_cat1 = ""
        self.active_cat2 = ""
        self.active_cat3 = ""
        self.active_cat4 = ""

        self.active_left_stat1 = ""
        self.active_left_stat2 = ""
        self.active_left_stat3 = ""
        self.active_left_stat4 = ""

        self.active_right_stat1 = ""
        self.active_right_stat2 = ""
        self.active_right_stat3 = ""
        self.active_right_stat4 = ""


    def reset_categories(self, *args):

        for index, this_cat in enumerate(DEFAULT_MATCHUP_CATS, 1):
            self.select_category(this_cat, index)


    def reset_preview(self, *args):

        self.preview_title = ""

        self.preview_left_player = None
        self.preview_right_player = None

        self.preview_left_participant_ID = 0
        self.preview_right_participant_ID = 0

        self.preview_left_player_name = ""
        self.preview_right_player_name = ""

        self.preview_left_champion = {}
        self.preview_right_champion = {}

        self.preview_left_stat1 = ""
        self.preview_left_stat2 = ""
        self.preview_left_stat3 = ""
        self.preview_left_stat4 = ""

        self.preview_right_stat1 = ""
        self.preview_right_stat2 = ""
        self.preview_right_stat3 = ""
        self.preview_right_stat4 = ""


    def update_active(self, *args):

        if "participants" in self.current_stats_update:
            left_participant = self.get_participant(
                self.current_stats_update["participants"],
                self.active_left_participant_ID
            )

            if left_participant is None:
                return

            right_participant = self.get_participant(
                self.current_stats_update["participants"],
                self.active_right_participant_ID
            )

            if right_participant is None:
                return

            for index, this_category in enumerate([
                self.active_cat1,
                self.active_cat2,
                self.active_cat3,
                self.active_cat4
            ], 1):

                self.get_stats("active", "left", this_category, index, left_participant, right_participant)
                self.get_stats("active", "right", this_category, index, right_participant, left_participant)


    def update_available_players(self, *args):
        self.available_left_players = [k for k,v in self.sorted_players if v.participant_ID < 6]
        self.available_right_players = [k for k,v in self.sorted_players if v.participant_ID >= 6]


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
                self.preview_left_participant_ID
            )

            if left_participant is None:
                return

            right_participant = self.get_participant(
                self.current_stats_update["participants"],
                self.preview_right_participant_ID
            )

            if right_participant is None:
                return

            for index, this_category in enumerate([
                self.preview_cat1,
                self.preview_cat2,
                self.preview_cat3,
                self.preview_cat4
            ], 1):

                self.get_stats("preview", "left", this_category, index, left_participant, right_participant)
                self.get_stats("preview", "right", this_category, index, right_participant, left_participant)


    def update_properties(self, *args):

        if self.visible:
            self.update_preview()

        if self.active:
            self.update_active()
