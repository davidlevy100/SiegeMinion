import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher

class AllPlayersOSCSender(DataEventDispatcher):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.player1 = PlayerOSCSender(source=self.app.overlay_players.player1)
        self.player2 = PlayerOSCSender(source=self.app.overlay_players.player2)
        self.player3 = PlayerOSCSender(source=self.app.overlay_players.player3)
        self.player4 = PlayerOSCSender(source=self.app.overlay_players.player4)
        self.player5 = PlayerOSCSender(source=self.app.overlay_players.player5)
        self.player6 = PlayerOSCSender(source=self.app.overlay_players.player6)
        self.player7 = PlayerOSCSender(source=self.app.overlay_players.player7)
        self.player8 = PlayerOSCSender(source=self.app.overlay_players.player8)
        self.player9 = PlayerOSCSender(source=self.app.overlay_players.player9)
        self.player10 = PlayerOSCSender(source=self.app.overlay_players.player10)


class PlayerOSCSender(DataEventDispatcher):

    local_time = kp.NumericProperty(0)
    participant_ID = kp.NumericProperty()
    source = kp.ObjectProperty()

    tricode = kp.StringProperty("")
    name = kp.StringProperty("")
    pick_champion = kp.DictProperty()
    championName = kp.StringProperty("")

    alive = kp.BooleanProperty(True)
    respawnTimer = kp.NumericProperty(0)
    
    level = kp.NumericProperty(0)

    health = kp.NumericProperty(0)
    health_max = kp.NumericProperty(1)

    primary_ability_resource = kp.NumericProperty(0)
    primary_ability_resource_max = kp.NumericProperty(1)

    spell1 = kp.DictProperty()
    summonerSpell1CooldownRemaining = kp.NumericProperty(0)
    summonerSpell1CooldownMax = kp.NumericProperty(1)

    spell2 = kp.DictProperty()
    summonerSpell2CooldownRemaining = kp.NumericProperty(0)
    summonerSpell2CooldownMax = kp.NumericProperty(1)

    ultimateName = kp.StringProperty("")
    ultimateCooldownRemaining = kp.NumericProperty(0)
    ultimateCooldownMax = kp.NumericProperty(1)

    primary_tree = kp.DictProperty()
    keystone = kp.DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.osc.setter('input_data'))

        self.app.livestats_history.bind(
            local_time=self.setter('local_time')
        )

    def on_source(self, *args):
        
        self.participant_ID = self.source.participant_ID

        self.source.bind(tricode=self.setter('tricode'))
        self.source.bind(name=self.setter('name'))
        self.source.bind(pick_champion=self.setter('pick_champion'))

        self.source.bind(alive=self.setter('alive'))
        self.source.bind(respawnTimer=self.setter('respawnTimer'))

        self.source.bind(level=self.setter('level'))
        
        self.source.bind(health=self.setter('health'))
        self.source.bind(health_max=self.setter('health_max'))
        
        self.source.bind(primary_ability_resource=self.setter('primary_ability_resource'))
        self.source.bind(primary_ability_resource_max=self.setter('primary_ability_resource_max'))
        
        self.source.bind(spell1=self.setter('spell1'))
        self.source.bind(summonerSpell1CooldownRemaining=self.setter('summonerSpell1CooldownRemaining'))
        self.source.bind(summonerSpell1CooldownMax=self.setter('summonerSpell1CooldownMax'))

        self.source.bind(spell2=self.setter('spell2'))
        self.source.bind(summonerSpell2CooldownRemaining=self.setter('summonerSpell2CooldownRemaining'))
        self.source.bind(summonerSpell2CooldownMax=self.setter('summonerSpell2CooldownMax'))

        self.source.bind(ultimateName=self.setter('ultimateName'))
        self.source.bind(ultimateCooldownRemaining=self.setter('ultimateCooldownRemaining'))
        self.source.bind(ultimateCooldownMax=self.setter('ultimateCooldownMax'))

        self.source.bind(primary_tree=self.setter('primary_tree'))
        self.source.bind(secondary_tree=self.setter('secondary_tree'))


    def send_name(self):

        index = self.participant_ID

        output = {
            f"/Overlay/Player{index}/name": f"{self.tricode} {self.name}"
        }

        self.send_data(**output)


    def on_championName(self, *args):

        index = self.participant_ID

        output = {
            f"/Overlay/Player{index}/champion": self.championName
        }

        self.send_data(**output)


    def on_alive(self, *args):

        index = self.participant_ID

        output = {
            f"/PlayerState/Player{index}": int(self.alive),
            f"/Overlay/Player{index}/alive": int(self.alive)
        }

        self.send_data(**output)

    
    def on_respawnTimer(self, *args):

        index = self.participant_ID

        output = {
            f"/Overlay/Player{index}/respawnTimer": self.respawnTimer
        }

        self.send_data(**output)


    def on_level(self, *args):

        index = self.participant_ID

        output = {
            f"/Overlay/Player{index}/level": self.level
        }

        self.send_data(**output)


    def on_health(self, *args):

        index = self.participant_ID

        output = {
            f"/Overlay/Player{index}/health": self.health
        }

        self.send_data(**output)


    def on_health_max(self, *args):

        index = self.participant_ID

        output = {
            f"/Overlay/Player{index}/healthMax": self.health_max
        }

        self.send_data(**output)


    def on_primary_ability_resource(self, *args):

        index = self.participant_ID

        output = {
            f"/Overlay/Player{index}/primaryAbilityResource": self.primary_ability_resource
        }

        self.send_data(**output)


    def on_primary_ability_resource_max(self, *args):

        index = self.participant_ID

        output = {
            f"/Overlay/Player{index}/primaryAbilityResourceMax": self.primary_ability_resource_max
        }

        self.send_data(**output)

    
    def on_spell1(self, *args):

        index = self.participant_ID

        output = {
            f"/Overlay/Player{index}/summonerSpell1Name": self.spell1["internal_name"]
        }

        self.send_data(**output)


    def on_summonerSpell1CooldownRemaining(self, *args):

        index = self.participant_ID

        output = {
            f"/Overlay/Player{index}/summonerSpell1CooldownRemaining": self.summonerSpell1CooldownRemaining
        }

        self.send_data(**output)


    def on_summonerSpell1CooldownMax(self, *args):

        index = self.participant_ID

        output = {
            f"/Overlay/Player{index}/summonerSpell1CooldownMax": self.summonerSpell1CooldownMax
        }

        self.send_data(**output)


    def on_spell2(self, *args):

        index = self.participant_ID

        output = {
            f"/Overlay/Player{index}/summonerSpell2Name": self.spell2["internal_name"]
        }

        self.send_data(**output)


    def on_summonerSpell2CooldownRemaining(self, *args):

        index = self.participant_ID

        output = {
            f"/Overlay/Player{index}/summonerSpell2CooldownRemaining": self.summonerSpell2CooldownRemaining
        }

        self.send_data(**output)


    def on_summonerSpell2CooldownMax(self, *args):

        index = self.participant_ID

        output = {
            f"/Overlay/Player{index}/summonerSpell2CooldownMax": self.summonerSpell2CooldownMax
        }

        self.send_data(**output)


    def on_ultimateName(self, *args):

        index = self.participant_ID

        output = {
            f"/Overlay/Player{index}/ultimateName": self.ultimateName
        }

        self.send_data(**output)


    def on_ultimateCooldownRemaining(self, *args):

        index = self.participant_ID

        output = {
            f"/Overlay/Player{index}/ultimateCooldownRemaining": self.ultimateCooldownRemaining
        }

        self.send_data(**output)


    def on_ultimateCooldownMax(self, *args):

        index = self.participant_ID

        output = {
            f"/Overlay/Player{index}/ultimateCooldownMax": self.ultimateCooldownMax
        }

        self.send_data(**output)


    def on_primary_tree(self, *args):

        index = self.participant_ID

        output = {
            f"/Overlay/Player{index}/primaryTree": self.primary_tree["internal_name"]
        }

        self.send_data(**output)


    def on_keystone(self, *args):

        index = self.participant_ID

        output = {
            f"/Overlay/Player{index}/keystone": self.keystone["internal_name"]
        }

        self.send_data(**output)


    def on_local_time(self, *args):
        
        self.send_name()
        self.on_championName()
        self.on_alive()
        self.on_respawnTimer()
        self.on_level()
        self.on_health()
        self.on_health_max()
        self.on_primary_ability_resource()
        self.on_primary_ability_resource_max()
        self.on_spell1()
        self.on_summonerSpell1CooldownRemaining()
        self.on_summonerSpell1CooldownMax()
        self.on_spell2()
        self.on_summonerSpell2CooldownRemaining()
        self.on_summonerSpell2CooldownMax()
        self.on_ultimateName()
        self.on_ultimateCooldownRemaining()
        self.on_ultimateCooldownMax()
        self.on_primary_tree()
        self.on_keystone()
