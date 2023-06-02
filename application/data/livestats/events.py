from kivy.app import App
from kivy.event import EventDispatcher
import kivy.properties as kp
from kivy.logger import Logger
from kivy.storage.jsonstore import JsonStore


def is_desired_event(**kwargs):

    """ returns True if a given event 
        contains all the keys and values
        given in kwargs
        else False """

    if "event" in kwargs:
        for k, v in kwargs.items():
            if k != "event":
                if k in kwargs["event"]:
                    if v != kwargs["event"][k]:
                        return False

                else:
                    return False

        return True
    
    else:
        return False


class LivestatsEventDispatcher(EventDispatcher):

    game_reset = kp.StringProperty("")
    output_reset = kp.StringProperty("")

    livestats_messages = kp.DictProperty()
    champ_select_event = kp.DictProperty()
    game_info_event = kp.DictProperty()
    latest_stats_update = kp.DictProperty()
    rift_herald_event = kp.DictProperty()
    baron_event = kp.DictProperty()
    elder_event = kp.DictProperty()
    dragon_event = kp.DictProperty()
    next_dragon_event = kp.DictProperty()
    inhibitor_event = kp.DictProperty()
    tower_event = kp.DictProperty()
    game_end_event = kp.DictProperty()
    pause_started_event = kp.DictProperty()
    stats_sequence_id = kp.NumericProperty()
    special_kill_event = kp.DictProperty()
    champion_kill_event = kp.DictProperty()

    item_destroyed_event = kp.DictProperty()
    item_purchased_event = kp.DictProperty()
    item_sold_event = kp.DictProperty()
    item_undo_event = kp.DictProperty()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = App.get_running_app()

        self.app.bind(game_reset=self.setter('game_reset'))

        self.app.livestats_poller.bind(
            output=self.setter('livestats_messages')
        )


    def on_livestats_messages(self, *args):

        """ Selects livestats events based on rfc461Schema and other 
            event properties.  Most common events are selected first.
            updates properties based on these events """

        
        if "events" in self.livestats_messages:
            for this_event in self.livestats_messages["events"]:

                ## Stats Update (most common event)
                if is_desired_event(
                    event = this_event,
                    rfc461Schema = "stats_update"
                ):
                    if ("sequenceIndex" in this_event and
                        this_event["sequenceIndex"] > self.stats_sequence_id
                    ):
                        self.stats_sequence_id = this_event["sequenceIndex"]
                        self.latest_stats_update = this_event


                ## Champ Select
                elif is_desired_event(
                    event = this_event,
                    rfc461Schema="champ_select"
                ):  
                    self.champ_select_event = this_event


                # Items

                ## Item Purchased
                elif is_desired_event(
                    event = this_event,
                    rfc461Schema="item_purchased",
                ):
                    self.item_purchased_event = this_event

                ## Item Destroyed
                elif is_desired_event(
                    event = this_event,
                    rfc461Schema="item_destroyed",
                ):
                    self.item_destroyed_event = this_event


                ## Item Sold
                elif is_desired_event(
                    event = this_event,
                    rfc461Schema="item_sold",
                ):
                    self.item_sold_event = this_event


                ## Item Undo
                elif is_desired_event(
                    event = this_event,
                    rfc461Schema="item_undo",
                ):
                    self.item_undo_event = this_event


                ## Turret Destroyed
                elif is_desired_event(
                    event = this_event,
                    rfc461Schema = "building_destroyed",
                    buildingType = "turret"
                ):
                    self.tower_event = this_event

                ## Inhibitor Destroyed
                elif is_desired_event(
                    event = this_event,
                    rfc461Schema = "building_destroyed",
                    buildingType = "inhibitor"
                ):
                    self.inhibitor_event = this_event

                ## Next Dragon
                elif is_desired_event(
                    event = this_event,
                    rfc461Schema = "queued_dragon_info"
                ):
                    self.next_dragon_event = this_event


                ## Special Kill
                elif is_desired_event(
                    event = this_event,
                    rfc461Schema="champion_kill_special",
                ):
                    self.special_kill_event = this_event


                ## Champion Kill
                elif is_desired_event(
                    event = this_event,
                    rfc461Schema="champion_kill",
                ):
                    self.champion_kill_event = this_event


                ## Rift Herald
                elif is_desired_event(
                    event = this_event,
                    rfc461Schema =  "epic_monster_kill",
                    monsterType = "riftHerald"
                ):
                    self.rift_herald_event = this_event

                ## Baron Kill
                elif is_desired_event(
                    event = this_event,
                    rfc461Schema =  "epic_monster_kill",
                    monsterType = "baron"
                ):
                    self.baron_event = this_event


                ## Elder dragon killed
                elif is_desired_event(
                    event = this_event,
                    rfc461Schema =  "epic_monster_kill",
                    monsterType = "dragon",
                    dragonType = "elder"
                ):
                    self.elder_event = this_event


                ## Regular Dragon Killed
                elif is_desired_event(
                    event = this_event,
                    rfc461Schema = "epic_monster_kill",
                    monsterType = "dragon"
                ):
                    self.dragon_event = this_event


                ## Game Info
                elif is_desired_event(
                    event = this_event,
                    rfc461Schema = "game_info"
                ):
                    if "gameVersion" in this_event:
                        self.game_version = this_event["gameVersion"]
                        
                    self.game_info_event = this_event


                ## Game End
                elif is_desired_event(
                    event = this_event,
                    rfc461Schema="game_end"
                ):
                    self.game_end_event = this_event


                ## Game Pause
                elif is_desired_event(
                    event = this_event,
                    rfc461Schema="pause_started"
                ):
                    self.pause_started_event = this_event

 
    def on_game_reset(self, *args):

        self.livestats_messages.clear()
        self.champ_select_event.clear()
        self.game_info_event.clear()
        self.latest_stats_update.clear()
        self.rift_herald_event.clear()
        self.baron_event.clear()
        self.elder_event.clear()
        self.dragon_event.clear()
        self.next_dragon_event.clear()
        self.inhibitor_event.clear()
        self.tower_event.clear()
        self.game_end_event.clear()
        self.pause_started_event.clear()
        self.stats_sequence_id = 0
        self.special_kill_event.clear()
        self.champion_kill_event.clear()
