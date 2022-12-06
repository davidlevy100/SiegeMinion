import kivy.properties as kp

from data.events.data_event_dispatch import DataEventDispatcher

from data.esports.stats import convert_milliseconds_to_HMS_string

class MythicItemVizSender(DataEventDispatcher):

    active = kp.BooleanProperty(False)

    mythic_item = kp.DictProperty({})
    participant_ID = kp.NumericProperty()
    stat_time = kp.NumericProperty(0)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.vizrt.setter('input_data'))

        self.app.mythic_item.bind(active=self.setter('active'))

        self.app.mythic_item.bind(mythic_item=self.setter('mythic_item'))
        self.app.mythic_item.bind(participant_ID=self.setter('participant_ID'))
        self.app.mythic_item.bind(stat_time=self.setter('stat_time'))

    
    def on_active(self, *args):

        output = {
            "sidepop/mastercard/anim": int(self.active),
        }

        self.send_data(**output)

    
    def on_mythic_item(self, *args):

        output = {
            "sidepop/mastercard/itemName": self.mythic_item.get("external_name", " "),
            "sidepop/mastercard/itemImage": self.mythic_item.get("internal_name", " ")
        }

        self.send_data(**output)


    def on_participant_ID(self, *args):

        output = {
            "sidepop/mastercard/player": self.participant_ID,
        }

        self.send_data(**output)


    def on_stat_time(self, *args):

        output = {
            "sidepop/mastercard/gameTime": convert_milliseconds_to_HMS_string(self.stat_time),
        }

        self.send_data(**output)
