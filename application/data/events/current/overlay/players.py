from math import sqrt

from collections import deque

import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher
from data.livestats.tools import parse_name

RelevantBuffs = {
    1680409346, # Kindred
    1467230133, # Draven
    3901057272, # Senna
    1960866709, # Veigar
    454914885, # Nasus
    2256731136, # Cho
    1721135316, # Bard
    3375836267, # Asol
    1911847746, # Sion
    2681101066, # Syndra
    2197950930, # Viktor
}

class OverlayPlayers(DataEventDispatcher):

    game_info_event = kp.DictProperty()

    runes_available = kp.BooleanProperty(False)

    player_map = kp.DictProperty({})
    sorted_players = kp.ListProperty([])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.live_data.bind(game_info_event=self.setter('game_info_event'))

        # Left Team Players
        self.player1 = OverlayPlayer(team_ID=100, participant_ID=1, lcu_source=self.app.lcu_champ_select.participant1)
        self.player2 = OverlayPlayer(team_ID=100, participant_ID=2, lcu_source=self.app.lcu_champ_select.participant2)
        self.player3 = OverlayPlayer(team_ID=100, participant_ID=3, lcu_source=self.app.lcu_champ_select.participant3)
        self.player4 = OverlayPlayer(team_ID=100, participant_ID=4, lcu_source=self.app.lcu_champ_select.participant4)
        self.player5 = OverlayPlayer(team_ID=100, participant_ID=5, lcu_source=self.app.lcu_champ_select.participant5)

        # Right Team Players
        self.player6 = OverlayPlayer(team_ID=200, participant_ID=6, lcu_source=self.app.lcu_champ_select.participant6)
        self.player7 = OverlayPlayer(team_ID=200, participant_ID=7, lcu_source=self.app.lcu_champ_select.participant7)
        self.player8 = OverlayPlayer(team_ID=200, participant_ID=8, lcu_source=self.app.lcu_champ_select.participant8)
        self.player9 = OverlayPlayer(team_ID=200, participant_ID=9, lcu_source=self.app.lcu_champ_select.participant9)
        self.player10 = OverlayPlayer(team_ID=200, participant_ID=10, lcu_source=self.app.lcu_champ_select.participant10)


    def on_game_reset(self, *args):

        self.player_map = {}
        self.sorted_players = []
        self.runes_available = False


    def on_game_info_event(self, *args):

        if "participants" in self.game_info_event:
            self.runes_available = True


    def update_player_map(self, player_name, player, *args):

        self.player_map[player_name] = player

        if len(self.player_map) >= 10:
            self.sorted_players = sorted(self.player_map.items(), key=lambda item: item[1].participant_ID)


    def find_player_by_name(self, name, *args):

        result = None

        for this_player in [
            self.player1,
            self.player2,
            self.player3,
            self.player4,
            self.player5,
            self.player6,
            self.player7,
            self.player8,
            self.player9,
            self.player10
        ]:
            if this_player.name == name:
                result = this_player

        return result


    def find_player_by_id(self, id, *args):

        result = None

        for this_player in [
            self.player1,
            self.player2,
            self.player3,
            self.player4,
            self.player5,
            self.player6,
            self.player7,
            self.player8,
            self.player9,
            self.player10
        ]:
            if this_player.participant_ID == id:
                result = this_player

        return result


class OverlayPlayer(DataEventDispatcher):

    lcu_source = kp.ObjectProperty()

    team_ID = kp.NumericProperty()
    participant_ID = kp.NumericProperty()

    game_info_event = kp.DictProperty()
    current_stats_update = kp.DictProperty()

    # Variables to Initialize
    tricode = kp.StringProperty("")
    name = kp.StringProperty("")
    pick_champion = kp.DictProperty()

    alive = kp.BooleanProperty(True)
    status_color = kp.ListProperty([1,1,1,1])

    level = kp.NumericProperty(0)

    health = kp.NumericProperty(0)
    health_max = kp.NumericProperty(1)
    health_percent = kp.NumericProperty(0)

    primary_ability_resource = kp.NumericProperty(0)
    primary_ability_resource_max = kp.NumericProperty(1)
    primary_ability_resource_percent = kp.NumericProperty(0)

    spell1 = kp.DictProperty()
    spell2 = kp.DictProperty()

    stats = kp.DictProperty()
    stat_time = kp.NumericProperty(0)


    #Runes
    primary_tree = kp.DictProperty()
    secondary_tree = kp.DictProperty()

    keystone = kp.DictProperty()

    rune1 = kp.DictProperty()
    rune2 = kp.DictProperty()
    rune3 = kp.DictProperty()
    rune4 = kp.DictProperty()
    rune5 = kp.DictProperty()

    stacks = kp.NumericProperty(-1)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app.live_data.bind(
            game_info_event=self.setter('game_info_event')
        )

        self.app.livestats_history.bind(
            current_stats_update=self.setter('current_stats_update')
        )

        self.inventory = Inventory(
            team_ID=self.team_ID,
            participant_ID=self.participant_ID,
            player=self
        )
        self.bind(stats=self.inventory.setter('stats'))
        self.bind(pick_champion=self.inventory.setter('pick_champion'))
        self.bind(stat_time=self.inventory.setter('stat_time'))

        self.lcu_source.bind(pick_champion=self.setter('pick_champion'))
        self.lcu_source.bind(spell1=self.setter('spell1'))
        self.lcu_source.bind(spell2=self.setter('spell2'))

    
    def on_alive(self, *args):

        if self.alive:
            self.status_color = [1,1,1,1]

        else:
            self.status_color = [1,0,0,1]

    
    def on_champion(self, *args):
        pass


    def on_game_reset(self, *args):

        self.tricode = ""
        self.name = ""
        self.pick_champion = self.app.data_dragon.get_asset("champion", "default")
        self.alive = True
        self.spell1 = self.app.data_dragon.get_asset("summoner_spell", "default")
        self.spell2 = self.app.data_dragon.get_asset("summoner_spell", "default")
        self.level = 0

        self.health = 0
        self.health_max = 1
        self.health_percent = 0

        self.primary_ability_resource = 0
        self.primary_ability_resource_max = 1
        self.primary_ability_resource_percent = 0

        self.primary_tree = self.app.data_dragon.get_asset("rune", "default")
        self.secondary_tree = self.app.data_dragon.get_asset("rune", "default")
        self.keystone = self.app.data_dragon.get_asset("rune", "default")

        self.rune1 = self.app.data_dragon.get_asset("rune", "default")
        self.rune2 = self.app.data_dragon.get_asset("rune", "default")
        self.rune3 = self.app.data_dragon.get_asset("rune", "default")
        self.rune4 = self.app.data_dragon.get_asset("rune", "default")
        self.rune5 = self.app.data_dragon.get_asset("rune", "default")

        self.stacks = -1


    def on_game_info_event(self, *args):

        if "participants" in self.game_info_event:

            this_participant = self.get_my_participant(
                self.game_info_event["participants"]
            )

            if this_participant is not None:
                self.get_name_and_champ(this_participant)
                self.get_runes(this_participant)


    def on_current_stats_update(self, *args):

        if "gameTime" in self.current_stats_update:
            self.stat_time = self.current_stats_update["gameTime"]

        if "participants" in self.current_stats_update:

            this_participant = self.get_my_participant(
                self.current_stats_update["participants"]
            )

            if this_participant is not None:

                if "summonerSpell1Name" in this_participant:

                    spell1 = self.app.data_dragon.get_asset(
                        "summoner_spell",
                        this_participant["summonerSpell1Name"]
                    )

                    if spell1 is not None:
                        self.spell1 = spell1


                if "summonerSpell2Name" in this_participant:

                    spell2 = self.app.data_dragon.get_asset(
                        "summoner_spell",
                        this_participant["summonerSpell2Name"]
                    )

                    if spell2 is not None:
                        self.spell2 = spell2
        

                if (len(self.name) == 0 or 
                    len(self.pick_champion) == 0
                ):
                    self.get_name_and_champ(this_participant)

                if "alive" in this_participant:
                    self.alive = this_participant["alive"]

                if "level" in this_participant:
                    self.level = this_participant["level"]

                if ("health" in this_participant and
                    "healthMax" in this_participant and
                    "primaryAbilityResource" in this_participant and
                    "primaryAbilityResourceMax" in this_participant
                ):
                    
                    self.health = this_participant["health"]
                    self.health_max = this_participant["healthMax"]
                    self.health_percent = min(1.0, (self.health / max(1, self.health_max)))

                    self.primary_ability_resource = this_participant["primaryAbilityResource"]
                    self.primary_ability_resource_max = this_participant["primaryAbilityResourceMax"]
                    self.primary_ability_resource_percent = min(1.0, (self.primary_ability_resource / max(1.0, self.primary_ability_resource_max)))                
                
                self.stats = this_participant

                if "stackingBuffs" in this_participant:
                    for buff in this_participant["stackingBuffs"]:
                        if buff["id"] in RelevantBuffs:
                            self.stacks = buff["stacks"]
                else:
                    self.stacks = -1


    def get_my_participant(self, participants, *args):

        result = None

        for this_participant in participants:
            if ("participantID" in this_participant and
                this_participant["participantID"] == self.participant_ID
            ):
                return this_participant

        return result


    def get_name_and_champ(self, participant, *args):

        raw_name = ""

        if "summonerName" in participant:

            raw_name = participant["summonerName"]


        elif "playerName" in participant:

            raw_name = participant["playerName"]


        if len(raw_name) > 0:

            tricode, name = parse_name(raw_name)

            if tricode is not None:
                self.tricode = tricode

            self.name = str(name)

            self.app.overlay_players.update_player_map(self.name, self)


        
        if "championName" in participant:

            champ = self.app.data_dragon.get_asset(
                "champion",
                participant["championName"]
            )

            if champ is not None:
                self.pick_champion = champ


    def get_runes(self, participant, *args):

        if "keystoneID" in participant:

            keystone = self.app.data_dragon.get_asset(
                "rune",
                participant["keystoneID"]
            )

            if keystone is not None:
                self.keystone = keystone 

        if ("perks" in participant and
            len(participant["perks"]) > 0 and
            "perkIds" in participant["perks"][0] and
            "perkStyle" in participant["perks"][0] and
            "perkSubStyle" in participant["perks"][0]
        ):

            primary_tree = self.app.data_dragon.get_asset(
                "rune",
                participant["perks"][0]["perkStyle"]
            )

            if primary_tree is not None:
                self.primary_tree = primary_tree

            secondary_tree = self.app.data_dragon.get_asset(
                "rune",
                participant["perks"][0]["perkSubStyle"]
            )

            if secondary_tree is not None:
                self.secondary_tree = secondary_tree

            for i in range(1, 6):

                this_rune = self.app.data_dragon.get_asset(
                    "rune",
                    participant["perks"][0]["perkIds"][i]
                )

                if this_rune is not None:
                    this_property = self.property(f"rune{i}")
                    this_property.set(self, this_rune)


class Inventory(DataEventDispatcher):

    team_ID = kp.NumericProperty()
    participant_ID = kp.NumericProperty()
    player = kp.ObjectProperty()

    store_tracker = kp.ObjectProperty()

    pick_champion = kp.DictProperty()

    item_callout_delay = kp.ConfigParserProperty(
        4.5,
        "User Game Data",
        "item_callout_delay",
        "app",
        val_type=float
    )

    stats = kp.DictProperty()
    stat_time = kp.NumericProperty(0)
    local_time = kp.NumericProperty(0)
    clock = kp.StringProperty("00:00")

    item0 = kp.DictProperty()
    item1 = kp.DictProperty()
    item2 = kp.DictProperty()
    item3 = kp.DictProperty()
    item4 = kp.DictProperty()
    item5 = kp.DictProperty()
    item6 = kp.DictProperty()

    callout_item = kp.DictProperty(allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.store_tracker = self.app.store_tracker

        self.default_item = self.app.data_dragon.get_asset(
            "item",
            "default"
        )

        self.app.top_bar.bind(clock=self.setter('clock'))

        self.app.livestats_history.bind(local_time=self.setter('local_time'))

        self.item_counts = {}
        self.callout_counts = {}

        self.callouts = deque()
        self.last_callout = 0
        self.item_list = []


    def on_game_reset(self, *args):

        for i in range(7):
            this_property = self.property(f"item{i}")
            this_property.set(self, self.default_item)

        self.item_counts.clear()
        self.callout_counts.clear()
        self.callout_item = None
        self.callouts.clear()
        self.last_callout = 0
        self.item_list = []


    def on_stats(self, *args):
        if "items" in self.stats:
            self.items = self.stats["items"]

            new_items = [self.default_item] * 7
            item_list = []
            self.item_counts.clear()

            for index, this_item in enumerate(self.stats["items"]):

                if "itemID" in this_item:

                    item_id = str(this_item["itemID"])

                    new_item = self.app.data_dragon.get_asset(
                        "item",
                        item_id
                    )

                    if item_id in self.item_counts:
                        self.item_counts[item_id] += 1

                    else:
                        self.item_counts[item_id] = 1

                    if new_item is not None:
                        new_items[index] = new_item
                        item_list.append(new_item)

                        if (self.out_of_fountain(self.stats) and 
                            self.is_callout(new_item) and
                            self.no_viego_issues(new_item)
                        ):
                            self.callouts.append(new_item)

                            if self.is_mythic_item(new_item):
                                self.app.mythic_item.set_mythic_item(self.team_ID, self.participant_ID, new_item, self.stat_time)
                                              
            self.item_list = item_list
            for index, this_item in enumerate(new_items):
                this_property = self.property(f"item{index}")
                this_property.set(self, this_item)


    def on_local_time(self, *args):

        if (len(self.callouts) > 0 and
            self.local_time - self.last_callout > (self.item_callout_delay * 1000)
        ):
            this_callout = self.callouts.popleft()

            self.callout_item = None
            self.callout_item = this_callout

            self.last_callout = self.local_time

            if "external_name" in this_callout:
                LogMessage = f'Item Callout: Siege Minion announced '
                LogMessage += f'{this_callout["external_name"]} at gametime: {self.clock}'
                Logger.info(LogMessage)


    def out_of_fountain(self, stats, *args):

        if ("alive" in stats and
            "teamID" in stats and
            "position" in stats and
            "x" in stats["position"] and
            "z" in stats["position"]
        ):

            if stats["alive"] == False:
                return False

            if stats["teamID"] == 100:

                if (stats["position"]["x"] > 1700 or
                    stats["position"]["z"] > 1750
                ):
                    return True

            elif stats["teamID"] == 200:

                if (stats["position"]["x"] < 12900 or
                    stats["position"]["z"] < 13200
                ):
                    return True

        return False


    def is_callout(self, item, *args):

        if ("code" in item and
            "tags" in item and
            "Callout" in item["tags"]
        ):

            if item["code"] not in self.callout_counts:
                self.callout_counts[item["code"]] = 1

                if ("external_name" in item and
                    "playerName" in self.stats
                ):
                    LogMessage = f'Item Callout: {self.stats["playerName"]} built '
                    LogMessage += f'{item["external_name"]} at gametime: {self.clock}'
                    Logger.info(LogMessage)

                return True

            elif (item["code"] in self.item_counts and
                self.callout_counts[item["code"]] < self.item_counts[item["code"]]
            ):
                self.callout_counts[item["code"]] += 1

                if ("external_name" in item and
                    "playerName" in self.stats
                ):
                    LogMessage = f'Item Callout: {self.stats["playerName"]} built '
                    LogMessage += f'{item["external_name"]} at gametime: {self.clock}'
                    Logger.info(LogMessage)

                return True

        return False

    
    def no_viego_issues(self, item):

        """ This function screens out issues caused by Viego
            inheriting his victim's items.

            If this is Viego, this function will call 
            the applications 'Store Tracker'to see if
            he really purchased the item in the inventory
        """

        result = False

        if ("external_name" in self.pick_champion and
            self.pick_champion["external_name"].lower() != "viego"
        ):
            result = True

        elif ("code" in item and
            item["code"].isnumeric()
        ):
            item_code = int(item["code"])
            result = self.store_tracker.did_purchase(self.participant_ID, item_code)

        return result


    def is_mythic_item(self, item):

        result = False

        if ("tags" in item and
            "Mythic" in item["tags"]
        ):
            result = True
        
        return result
