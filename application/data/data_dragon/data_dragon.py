from pathlib import Path
from datetime import datetime
from functools import partial

from kivy.event import EventDispatcher
import kivy.properties as kp
from kivy.logger import Logger
from kivy.storage.jsonstore import JsonStore
from kivy.network.urlrequest import UrlRequest
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.settings import SettingSpacer
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout


VERSIONS_URL = "https://ddragon.leagueoflegends.com/api/versions.json"
CDN = "http://ddragon.leagueoflegends.com/cdn"
CHAMPS = "data/en_US/champion.json"
RUNES = "data/en_US/runesReforged.json"
SUMMONERS = "data/en_US/summoner.json"
ITEMS = "data/en_US/item.json"

RUNE_PATH = Path().joinpath('ui', 'images', 'Runes')
RUNE_PLACEHOLDER = "_RunePlaceholder"
DEFAULT_RUNE = {
    "code": -1,
    "internal_name": RUNE_PLACEHOLDER,
    "external_name": "",
    "rune_type": "",
    "local_image_path": RUNE_PATH.joinpath(f"{RUNE_PLACEHOLDER}.png"),
    "long_name": RUNE_PLACEHOLDER
}

CHAMP_PATH = Path().joinpath('ui', 'images', 'ChampIcons')
CHAMP_PLACEHOLDER = "_Placeholder"
DEFAULT_CHAMP = {
    "code": "-1",
    "internal_name": CHAMP_PLACEHOLDER,
    "external_name": "",
    "local_image_path": CHAMP_PATH.joinpath(f"{CHAMP_PLACEHOLDER}.png")
}


SPLASH_PATH = Path().joinpath('ui', 'images', 'SplashCentered')
SPLASH_PLACEHOLDER = "_Placeholder"

SUMMONER_PATH = Path().joinpath('ui', 'images', 'SummonerSpells')
SUMMONER_PLACEHOLDER = "_Placeholder"
DEFAULT_SUMMONER_SPELL = {
    "code": "-1",
    "internal_name": SUMMONER_PLACEHOLDER,
    "external_name": SUMMONER_PLACEHOLDER,
    "local_image_path": SUMMONER_PATH.joinpath(f"{SUMMONER_PLACEHOLDER}.png")
}

ITEM_PATH = Path().joinpath('ui', 'images', 'Items')
ITEM_PLACEHOLDER = "_Placeholder"
DEFAULT_ITEM = {
    "code": "-1",
    "internal_name": ITEM_PLACEHOLDER,
    "external_name": "",
    "local_image_path": ITEM_PATH.joinpath(f"{ITEM_PLACEHOLDER}.png"),
    "tags": []
}

HEADERS = {
    'Accept': "application/json",
    'Cache-Control': "no-cache",
    'cache-control': "no-cache",
    'Host': "ddragon.leagueoflegends.com"
}

IMG_HEADERS = {
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'cache-control': "no-cache",
    'Host': "ddragon.leagueoflegends.com"
}


def get_item_internal_name(**kwargs):

    if "item" in kwargs:
        item = kwargs["item"]

        allowed_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

        new_name = ''.join(x for x in item if x in allowed_chars)

        return new_name


def get_rune_long_name(**kwargs):

    if ("rune_family" in kwargs and
        "rune" in kwargs
    ):
        rune = kwargs["rune"]

        allowed_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        new_name = ''.join(x for x in rune if x in allowed_chars)

        return f"{kwargs['rune_family']}_{new_name}"

    elif "rune_family" in kwargs:
        return kwargs["rune_family"]


class PopupLabel(Label):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_texture_size(self, *args):
        self.height = self.texture_size[1]


class DataDragon(EventDispatcher):

    version = kp.StringProperty("")
    config_version = kp.ConfigParserProperty(
        "",
        "Data Dragon",
        "game_version",
        "app"
    )


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.champions = JsonStore(f"{Path().joinpath('data', 'storage', 'champions.json')}")
        self.runes = JsonStore(f"{Path().joinpath('data', 'storage', 'runes.json')}")
        self.summoner_spells = JsonStore(f"{Path().joinpath('data', 'storage', 'summoner_spells.json')}")
        self.items = JsonStore(f"{Path().joinpath('data', 'storage', 'items.json')}")

        self.content = GridLayout(cols=1, spacing='5dp')

        self.popup_text = PopupLabel(
            size_hint=(1, None),
            text="Data Dragon",
            text_size=(None, None)
        )

        self.scroll_content = ScrollView(
            bar_width = 4,
            scroll_type=['bars', 'content']
        )

        self.scroll_content.add_widget(self.popup_text)

        self.content.add_widget(self.scroll_content)

        self.popup = Popup(
            title='New game version detected, please wait.',
            content = self.content,
            size_hint=(0.5, 0.5)
        )

        self.spacer = SettingSpacer()
        self.button = Button(
            text='Close',
            size=(
                self.popup.width, 
                dp(50)
            ),
            size_hint=(0.9, None)
        )
        self.button.bind(on_release=self.popup.dismiss)

        self.popup.content.add_widget(self.spacer)
        self.popup.content.add_widget(self.button)

    
    def on_config_version(self, *args):
        self.check_version(version=self.config_version)


    def on_version(self, *args):

        self.popup_text.text = ""
        self.popup.open()

        function_map = {
            CHAMPS: self.process_champions,
            RUNES: self.process_runes,
            SUMMONERS: self.process_summoner_spells,
            ITEMS: self.process_items
        }

        for this_data, this_function in function_map.items():

            url = f"{CDN}/{self.version}/{this_data}"

            self.get_data(
                url=url,
                headers=HEADERS,
                function=this_function
            )


    def storage_report(self, store, key, result):

        store_type = ""

        if store is self.champions:
            store_type = "Champion "
        elif store is self.runes:
            store_type = "Rune "
        elif store is self.summoner_spells:
            store_type = "Summoner Spell "
        elif store is self.items:
            store_type = "Item "

        LogMessage = "Data Dragon: "

        if result:
            LogMessage += f"Storing {store_type}{key}."
        else:
            LogMessage += f"Attempt to store {store_type}{key} failed."

        Logger.info(LogMessage)

        
    def check_version(self, *args, **kwargs):

        """ expects a version number with at least 2 sections
            i.e. 9.12, or 9.12.223.444
            upon success will make a urlrequest to ddragon
            and send result to self.check_ddragon_versions """

        if "version" in kwargs:

            version_sections = kwargs["version"].split(".")[:2]

            if len(version_sections) < 2:
                Logger.exception("Error: Improper Version Number - expecting at least 2 numbers separated by a period")
                return

            for this_section in version_sections:
                if not this_section.isdigit():
                    Logger.exception("Error: Improper Version Number - expecting at least 2 numbers separated by a period")
                    return

            version = ".".join(version_sections)

            self.get_data(
                url=VERSIONS_URL,
                headers=HEADERS,
                function=partial(
                    self.check_ddragon_versions,
                    version = version
                )
            )
        
        else:
            return

    
    def match_versions(self, **kwargs):

        """ expects a properly formatted local version
            and a descending sorted list of versions from ddragon """

        if ("local_version" in kwargs and
            "ddragon_versions" in kwargs
        ):

            local_version = kwargs["local_version"]
            ddragon_versions = kwargs["ddragon_versions"]

            for this_version in sorted(ddragon_versions, reverse=True):
                if ".".join(this_version.split(".")[:2]) == local_version:
                    return this_version

        return


    def check_ddragon_versions(self, request, result, **kwargs):

        if ("version" in kwargs and 
            len(result) > 0    
        ):
            ddragon_version = self.match_versions(
                local_version=kwargs["version"],
                ddragon_versions=result
            )

            if ddragon_version is not None:
                self.version = ddragon_version

        return


    def get_image(self, **kwargs):
        
        if ("image" in kwargs and
            "image_type" in kwargs and
            "path" in kwargs          
        ):
            image = kwargs["image"]
            path = kwargs["path"]
            image_type = kwargs["image_type"]

            if image_type == "runes":
                url = f"{CDN}/img/{image}"
            else:
                url = f"{CDN}/{self.version}/img/{image_type}/{image}"
            
            image_filename = kwargs["image"].split("/")[-1]

            file_path = f"{path.joinpath(image_filename)}"

        UrlRequest(
            url,
            file_path=file_path,
            on_success = partial(
                self.got_image,
                image=image
            ), 
            on_redirect = self.got_redirect,
            on_failure = self.got_fail,
            on_error = self.got_error,
            req_headers = IMG_HEADERS,
            verify = False
        )


    def got_image(self, *args, **kwargs):

        if "image" in kwargs:
            image = kwargs["image"]

            LogMessage = (
                f"Data Dragon: Downloaded {image}"
            )
            Logger.info(LogMessage)


    def have_image(self, **kwargs):

        if ("image" in kwargs and
            "path" in kwargs          
        ):
            image = kwargs["image"].split("/")[-1]
            path = kwargs["path"]

            my_file = path.joinpath(image)

            return my_file.is_file()


    def process_champions(self, request, result):

        self.popup_text.text += "\n\nChampions Downloaded\n\n"
        
        if (len(result) > 0 and
            "data" in result
        ):
            for this_champion_data in result["data"].values():
                if ("id" in this_champion_data and
                    "key" in this_champion_data and
                    "name" in this_champion_data and
                    "image" in this_champion_data and
                    "full" in this_champion_data["image"]
                ):
                    this_internal_name = this_champion_data["id"]
                    this_code = this_champion_data["key"]
                    this_external_name = this_champion_data["name"]
                    this_image = this_champion_data["image"]["full"]

                    if not self.have_image(path=CHAMP_PATH, image=this_image):
                        self.get_image(path=CHAMP_PATH, image=this_image, image_type="champion")


                    self.champions.async_put(
                        callback=self.storage_report,
                        key=f"{this_internal_name}".lower(),
                        code=this_code,
                        internal_name=this_internal_name,
                        external_name=this_external_name,
                        local_image_path=f"{CHAMP_PATH.joinpath(this_image)}"
                    )

                    self.champions.async_put(
                        callback=self.storage_report,
                        key=this_code,
                        code=this_code,
                        internal_name=this_internal_name,
                        external_name=this_external_name,
                        local_image_path=f"{CHAMP_PATH.joinpath(this_image)}"
                    )

            #Add default Champ
            self.champions.async_put(
                callback=self.storage_report,
                key="default",
                code="-1",
                internal_name=CHAMP_PLACEHOLDER,
                external_name="",
                local_image_path=f"{CHAMP_PATH.joinpath(CHAMP_PLACEHOLDER)}.png"
            )

            #Add null Champ
            self.champions.async_put(
                callback=self.storage_report,
                key="",
                code="-1",
                internal_name=CHAMP_PLACEHOLDER,
                external_name="",
                local_image_path=f"{CHAMP_PATH.joinpath(CHAMP_PLACEHOLDER)}.png"
            )


            if "version" in result:
                self.champions.async_put(
                    callback=self.storage_report,
                    key="version",
                    version=result["version"]
                )

            LogMessage = (
                f"Data Dragon: "
                f"updated Champion info to "
                f"requested version: {self.version}"
            )
            Logger.info(LogMessage)
            

    def process_runes(self, request, result):

        self.popup_text.text += "\n\nRunes Downloaded\n\n"
        
        if len(result) > 0:

            for this_rune_family in result:

                if ("id" in this_rune_family and
                    "name" in this_rune_family and
                    "icon" in this_rune_family
                ):

                    this_rune_family_code = this_rune_family["id"]
                    this_rune_family_name = this_rune_family["name"]
                    this_rune_family_image = this_rune_family["icon"]
                    this_local_rune_family_image_path = this_rune_family_image.split("/")[-1]
                    this_rune_family_long_name = get_rune_long_name(
                        rune_family=this_rune_family_name
                    )

                    if not self.have_image(path=RUNE_PATH, image=this_rune_family_image):
                        self.get_image(path=RUNE_PATH, image=this_rune_family_image, image_type="runes")

                    self.runes.async_put(
                        callback=self.storage_report,
                        key=this_rune_family_code,
                        code=this_rune_family_code,
                        internal_name=this_rune_family_name,
                        external_name=this_rune_family_name,
                        rune_type=this_rune_family_name,
                        local_image_path=f"{RUNE_PATH.joinpath(this_local_rune_family_image_path)}",
                        long_name=this_rune_family_long_name
                    )

                    if "slots" in this_rune_family:
                        for this_slot in this_rune_family["slots"]:
                            if "runes" in this_slot:
                                for this_rune in this_slot["runes"]:

                                    if ("id" in this_rune and
                                        "key" in this_rune and
                                        "name" in this_rune and
                                        "icon" in this_rune
                                    ):

                                        this_rune_code = this_rune["id"]
                                        this_rune_internal_name = this_rune["key"]
                                        this_rune_external_name = this_rune["name"]
                                        this_rune_image = this_rune["icon"]
                                        this_local_rune_image_path = this_rune_image.split("/")[-1]
                                        this_rune_long_name = get_rune_long_name(
                                            rune=this_rune_external_name,
                                            rune_family=this_rune_family_name
                                        )

                                        if not self.have_image(path=RUNE_PATH, image=this_rune_image):
                                            self.get_image(path=RUNE_PATH, image=this_rune_image, image_type="runes")

                                        self.runes.async_put(
                                            callback=self.storage_report,
                                            key=this_rune_code,
                                            code=this_rune_code,
                                            internal_name=this_rune_internal_name,
                                            external_name=this_rune_external_name,
                                            rune_type=this_rune_family_name,
                                            local_image_path=f"{RUNE_PATH.joinpath(this_local_rune_image_path)}",
                                            long_name=this_rune_long_name
                                        )

            #Add Default Rune
            self.runes.async_put(
                callback=self.storage_report,
                key="default",
                code=-1,
                internal_name=RUNE_PLACEHOLDER,
                external_name="",
                rune_type="",
                local_image_path=f"{RUNE_PATH.joinpath(RUNE_PLACEHOLDER)}.png",
                long_name=RUNE_PLACEHOLDER
            )

            #Add Null Rune
            self.runes.async_put(
                callback=self.storage_report,
                key="",
                code=-1,
                internal_name=RUNE_PLACEHOLDER,
                external_name="",
                rune_type="",
                local_image_path=f"{RUNE_PATH.joinpath(RUNE_PLACEHOLDER)}.png",
                long_name=RUNE_PLACEHOLDER
            )

            self.runes.async_put(
                callback=self.storage_report,
                key="-1",
                code=-1,
                internal_name=RUNE_PLACEHOLDER,
                external_name="",
                rune_type="",
                local_image_path=f"{RUNE_PATH.joinpath(RUNE_PLACEHOLDER)}.png",
                long_name=RUNE_PLACEHOLDER
            )

            self.runes.async_put(
                callback=self.storage_report,
                key="version",
                version=self.version
            )

            LogMessage = (
                f"Data Dragon: "
                f"updated Runes info to "
                f"requested version: {self.version}"
            )
            Logger.info(LogMessage)


    def process_summoner_spells(self, request, result):

        self.popup_text.text += "\n\nSummoner Spells Downloaded\n\n"
        
        if (len(result) > 0 and
            "data" in result    
        ):
            for this_summoner_data in result["data"].values():
                
                if ("id" in this_summoner_data and
                    "key" in this_summoner_data and
                    "name" in this_summoner_data and
                    "image" in this_summoner_data and
                    "full" in this_summoner_data["image"]
                ):

                    this_internal_name = this_summoner_data["id"]
                    this_code = this_summoner_data["key"]
                    this_external_name = this_summoner_data["name"]
                    this_image = this_summoner_data["image"]["full"]

                    if not self.have_image(path=SUMMONER_PATH, image=this_image):
                        self.get_image(path=SUMMONER_PATH, image=this_image, image_type="spell")

                    self.summoner_spells.async_put(
                        callback=self.storage_report,
                        key=this_code,
                        code=this_code,
                        internal_name=this_internal_name,
                        external_name=this_external_name,
                        local_image_path=f"{SUMMONER_PATH.joinpath(this_image)}"
                    )

                    self.summoner_spells.async_put(
                        callback=self.storage_report,
                        key=this_internal_name,
                        code=this_code,
                        internal_name=this_internal_name,
                        external_name=this_external_name,
                        local_image_path=f"{SUMMONER_PATH.joinpath(this_image)}"
                    )

            # add default summoner spell
            self.summoner_spells.async_put(
                callback=self.storage_report,
                key="default",
                code="-1",
                internal_name=SUMMONER_PLACEHOLDER,
                external_name="",
                local_image_path=f"{SUMMONER_PATH.joinpath(SUMMONER_PLACEHOLDER)}.png"
            )

            # add null summoner spell
            self.summoner_spells.async_put(
                callback=self.storage_report,
                key="",
                code="-1",
                internal_name=SUMMONER_PLACEHOLDER,
                external_name="",
                local_image_path=f"{SUMMONER_PATH.joinpath(SUMMONER_PLACEHOLDER)}.png"
            )

            if "version" in result:
                self.summoner_spells.async_put(
                    callback=self.storage_report,
                    key="version",
                    version=result["version"]
                )

            LogMessage = (
                f"Data Dragon: "
                f"updated Summoner spell info to "
                f"requested version: {self.version}"
            )
            Logger.info(LogMessage)

    
    def get_enchantment_name(self, item, items_dict):

        prefix = ""
        suffix = ""

        name = ""

        external_name = ""
        internal_name = ""

        if "name" in item:
            name = item["name"]

        if ":" in name:
            suffix = f': {name.split(":")[1].strip()}'

        #find prefix

        if "from" in item:
            for this_id in item["from"]:
                if (this_id in items_dict and
                    "tags" in items_dict[this_id] and
                    "Jungle" in items_dict[this_id]["tags"] and 
                    "name" in items_dict[this_id]
                ):
                    prefix = items_dict[this_id]["name"]

        if len(prefix) > 3:
            external_name = f"{prefix}{suffix}"
            internal_name = get_item_internal_name(
                item=f"{prefix[:4]}{suffix}"
            )

        else:
            external_name = name
            internal_name = get_item_internal_name(
                item=external_name
            )

        return external_name, internal_name


    def is_callout(self, item, items_dict):

        exceptions = [
            "Mejai's Soulstealer",
            "Enchantment: Warrior",
            "Enchantment: Cinderhulk",
            "Enchantment: Runic Echoes",
            "Enchantment: Bloodrazor",
            "Skirmisher's Sabre",
            "Stalker's Blade",
            "Harrowing Crescent",
            "Frostfang",
            "Runesteel Spaulders",
            "Targon's Buckler",
            "Black Mist Scythe",
            "Bulwark of the Mountain",
            "Pauldrons of Whiterock",
            "Shard of True Ice"
        ]

        result = False
        passed_gold = False
        passed_depth = False
        passed_into = False

        #Exception Test

        if ("name" in item and
            item["name"] in exceptions
        ):
            return True

        # Gold Test - Gold total > 1500 passes
        if ("gold" in item and
            "total" in item["gold"] and
            item["gold"]["total"] > 1500
        ):
            passed_gold = True

        else:
            return False

        # Depth Test - no depth or depth > 2 passes
        if ("depth" in item and
            item["depth"] < 2
        ):
            return False

        else:
            passed_depth = True


        # Ornn test - weed out Ornn Items

        if ("requiredAlly" in item and
            item["requiredAlly"] == "Ornn"
        ):
            return False

        else:
            passed_ornn = True


        # Builds Into Test - doesn't build into anything or
        # builds only into Ornn Item

        if ("into" not in item or
            len(item["into"]) == 0
        ):
            passed_into = True

        else:

            if len(item["into"]) > 1: 
                return False

            context_item = {}

            if str(item["into"][0]) in items_dict:
                context_item = items_dict[str(item["into"][0])]

            else:
                return False

            if ("requiredAlly" in context_item and
                context_item["requiredAlly"] == "Ornn"
            ):
                passed_into = True
            
            else:
                return False


        result = (passed_gold and passed_depth and passed_into and passed_ornn)

        return result


    def is_mythic(self, item):

        result = False

        if ("description" in item and
            "rarityMythic" in item["description"]
        ):
            result = True

        return result


    def process_items(self, request, result):

        self.popup_text.text += "\n\nItems Downloaded\n\n"
        
        if (len(result) > 0 and
            "data" in result    
        ):

            for key, value in result["data"].items():

                if ("name" in value and
                    "image" in value and
                    "full" in value["image"] and
                    "tags" in value
                ):

                    this_name = value["name"]

                    if "enchantment:" in this_name.lower():
                        external_name, internal_name = self.get_enchantment_name(
                            value, 
                            result["data"]
                        )

                    else:
                        external_name = this_name
                        internal_name = get_item_internal_name(item=this_name)


                    this_image = value["image"]["full"]
                    these_tags = value["tags"]

                    callout = self.is_callout(value, result["data"])

                    if callout:
                        these_tags.append("Callout")

                    mythic = self.is_mythic(value)

                    if mythic:
                        these_tags.append("Mythic")
                    

                    if not self.have_image(path=ITEM_PATH, image=this_image):
                        self.get_image(path=ITEM_PATH, image=this_image, image_type="item")

                    self.items.async_put(
                        callback=self.storage_report,
                        key=key,
                        code=key,
                        internal_name=internal_name,
                        external_name=external_name,
                        local_image_path=f"{ITEM_PATH.joinpath(this_image)}",
                        tags=these_tags
                    )

            # add default item
            self.items.async_put(
                callback=self.storage_report,
                key="default",
                code="-1",
                internal_name=ITEM_PLACEHOLDER,
                external_name="",
                local_image_path=f"{ITEM_PATH.joinpath(ITEM_PLACEHOLDER)}.png",
                tags=[]
            )

            # add null item
            self.items.async_put(
                callback=self.storage_report,
                key="",
                code="-1",
                internal_name=ITEM_PLACEHOLDER,
                external_name="",
                local_image_path=f"{ITEM_PATH.joinpath(ITEM_PLACEHOLDER)}.png",
                tags=[]
            )

            if "version" in result:
                self.items.async_put(
                    callback=self.storage_report,
                    key="version",
                    version=result["version"]
                )

            LogMessage = (
                f"Data Dragon: "
                f"updated item info to "
                f"requested version: {self.version}"
            )
            Logger.info(LogMessage)

    
    def get_data(self, **kwargs):

        """ Single Function to GET data
            Expects full URL(url), 
            headers(headers), 
            and the function
            to send data to (function) """

        url = kwargs["url"]
        headers = kwargs["headers"]
        function = kwargs["function"]

        UrlRequest(
            url,
            on_success = function,
            on_redirect = self.got_redirect,
            on_failure = self.got_fail,
            on_error = self.got_error,
            req_headers = headers,
            verify = False
        )


    def got_error(self, req, *args):
        self.myStatus = [0.5, 0, 0, 1]
        Logger.exception(f"Data Dragon Error: {datetime.now().strftime('%r')} {req.url}, {args}")
        return


    def got_fail(self, req, *args):
        self.myStatus = [0.5, 0, 0, 1]
        Logger.exception(f"Data Dragon Fail: {datetime.now().strftime('%r')} {req.url}, {args}")
        return


    def got_redirect(self, req, *args):
        Logger.exception(f"Data Dragon Redirect: {datetime.now().strftime('%r')} {req.url}, {args}")
        return


    def get_asset(self, asset_type, asset_name):

        """ expects champion, rune, summoner_spell or item
            will return the proper asset from the proper store
            returns None if not found """

        asset = None
        asset_store = None

        if asset_type == "champion":
            asset = asset_name.lower()
            asset_store = self.champions

        elif asset_type == "rune":
            asset = asset_name
            asset_store = self.runes

        elif asset_type == "summoner_spell":
            asset = asset_name
            asset_store = self.summoner_spells

        elif asset_type == "item":
            asset = asset_name
            asset_store = self.items

        if (asset is not None and
            asset_store is not None
        ):

            asset_string = str(asset)
            if asset_string in asset_store:
                return asset_store[asset_string]
            
        return None
