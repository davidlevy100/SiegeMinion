from kivy.app import App
from kivy.uix.image import Image, AsyncImage
import kivy.properties as kp
from kivy.logger import Logger

from ui.constants.images import PLACEHOLDER_IMAGE

class GameImage(Image):

    asset_name = kp.StringProperty()
    asset_type = kp.StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.source = PLACEHOLDER_IMAGE


    def on_asset_name(self, *args):
        self.get_image(self.asset_name)


    def get_image(self, name, *args):

        image_source = self.app.data_dragon.get_asset(
            self.asset_type,
            name
        )

        if image_source is not None:
            self.source = image_source["local_image_path"]

        else:
            self.source = PLACEHOLDER_IMAGE

            LogMessage = "Image Error: "
            LogMessage += f"couldn't find image {name} "
            LogMessage += f"for {self}"

            Logger.exception(LogMessage)


class ChampionImage(GameImage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.asset_type = "champion"


class RuneImage(GameImage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.asset_type = "rune"


class SummonerSpellImage(GameImage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.asset_type = "summoner_spell"


class ItemImage(GameImage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.asset_type = "item"


class OverlayImage(Image):

    asset = kp.DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.source = PLACEHOLDER_IMAGE


    def on_asset(self, *args):

        if "local_image_path" in self.asset:
            self.source = self.asset["local_image_path"]

        else:
            self.source = PLACEHOLDER_IMAGE

