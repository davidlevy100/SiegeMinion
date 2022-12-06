import kivy.properties as kp

from data.events.data_event_dispatch import DataEventDispatcher

class SpecialBaronAnnounceVizSender(DataEventDispatcher):

    active = kp.BooleanProperty(False)
    baron_stolen = kp.BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.vizrt.setter('input_data'))

        self.active = self.app.special_baron_announce_event.active
        self.app.special_baron_announce_event.bind(active=self.setter('active'))

        self.baron_stolen = self.app.special_baron_announce_event.baron_stolen
        self.app.special_baron_announce_event.bind(baron_stolen=self.setter('baron_stolen'))


    def on_active(self, *args):

        output = {
            "bpp/anim": int(self.active),
            "bpp/steal": int(self.baron_stolen)
        }

        self.send_data(**output)


    def on_baron_stolen(self, *args):

        output = {
            "bpp/steal": int(self.baron_stolen),
        }

        self.send_data(**output)
