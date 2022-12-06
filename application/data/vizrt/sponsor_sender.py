import kivy.properties as kp

from data.events.data_event_dispatch import DataEventDispatcher


class SponsorSender(DataEventDispatcher):

    active = kp.BooleanProperty(False)
    target = kp.ObjectProperty()
    key = kp.StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.vizrt.setter('input_data'))

    def on_target(self, *args):
        self.target.bind(active=self.setter('active'))

    def on_active(self, *args):

        output = {
            self.key: int(self.active)
        }

        self.send_data(**output)
