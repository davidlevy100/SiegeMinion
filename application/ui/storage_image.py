from kivy.uix.image import Image
import kivy.properties as kp


class StorageImage(Image):

    asset = kp.DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if "local_image_path" in self.asset:
            self.source = self.asset["local_image_path"]

    def on_asset(self, *args):

        if "local_image_path" in self.asset:
            self.source = self.asset["local_image_path"]
