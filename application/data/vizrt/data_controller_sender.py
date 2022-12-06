
import kivy.properties as kp
from kivy.logger import Logger

from data.events.data_event_dispatch import DataEventDispatcher


class DataControllerVizSender(DataEventDispatcher):

    active = kp.BooleanProperty(False)
    source = kp.ObjectProperty()
    key = kp.StringProperty("")


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(output=self.app.vizrt.setter('input_data'))


    def on_active(self, *args):

        output = {
            self.key: int(self.active)
        }
        self.send_data(**output)


    def on_source(self, *args):

        active = self.source.active
        self.source.bind(active=self.setter('active'))