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

    ultimate = kp.DictProperty()
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

        self.source.bind(ultimate=self.setter('ultimate'))
        self.source.bind(ultimateCooldownRemaining=self.setter('ultimateCooldownRemaining'))
        self.source.bind(ultimateCooldownMax=self.setter('ultimateCooldownMax'))

        self.source.bind(primary_tree=self.setter('primary_tree'))
        self.source.bind(secondary_tree=self.setter('secondary_tree'))


    def on_alive(self, *args):

        output = {
            f"/PlayerState/Player{self.participant_ID}": int(self.alive)
        }

        self.send_data(**output)


    def on_local_time(self, *args):
        self.on_alive()
