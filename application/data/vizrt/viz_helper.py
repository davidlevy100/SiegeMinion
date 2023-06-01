from pathlib import Path

from kivy.logger import Logger

RUNE_PATH = ".\\images\\Runes"
RUNE_PLACEHOLDER = "_RunePlaceholder"

CHAMP_PATH = ".\\images\\ChampIcons"
CHAMP_PLACEHOLDER = "_banPlaceholder"

SPLASH_PATH = ".\\images\\SplashCentered"
SPLASH_PLACEHOLDER = "_Placeholder"

SUMMONER_PATH = ".\\images\\SummonerSpells"
SUMMONER_PLACEHOLDER = "_Placeholder"

DRAGON_CODES = {
    "": 0,
    None: 0,
    "default": 0,
    "air": 1,
    "cloud": 1,
    "fire": 2,
    "infernal": 2,
    "earth": 3,
    "mountain": 3,
    "water": 4,
    "ocean": 4,
    "chemtech": 5,
    "hextech": 6,
    "elder": 7,
}

PASSIVES = {
    "aurelionsol": "AurelionSolPassive",
    "bard": "BardPassive",
    "chogath": "ChoGathFeast",
    "draven": "DravenPassive",
    "kindred": "KindredPassive",
    "nasus": "NasusSiphoningStrike",
    "senna": "SennaPassive",
    "sion": "SionSoulFurnace",
    "syndra": "SyndraPassive",
    "syndra2": "SyndraPassive2",
    "veigar": "VeigarPassive",
    "viktor": "ViktorPassive"
}

def get_dragon_code(dragon_name):

    if dragon_name in DRAGON_CODES:
        return DRAGON_CODES[dragon_name]
    else:
        LogMessage = f"Unknown Dragon {dragon_name}"
        Logger.exception(f"Error: {LogMessage}")
        return DRAGON_CODES["default"]



def vizify_rune(**kwargs):

    if "rune" in kwargs:

        rune = kwargs["rune"]

        allowed_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

        try:

            newName = ''.join(x for x in rune["name"] if x in allowed_chars)

            if 'runeType' in rune:
                return f"{rune['runeType']}_{newName}"
            else:
                return f"{rune['key']}"

        except Exception as e:
            Logger.exception(f"Error: {e}")
            return ""

    else:
        LogMessage = f"No rune given"
        Logger.exception(f"Error: {LogMessage}")
        return ""


def get_rune_image_path(**kwargs):

    if "rune" in kwargs:
        rune = kwargs["rune"]

    else:
        LogMessage = f"No rune given"
        Logger.exception(f"Error: {LogMessage}")
        return f"{RUNE_PATH}\\{RUNE_PLACEHOLDER}"

    myPath = f"{RUNE_PATH}\\{vizify_rune(rune=rune)}.png"

    my_file = Path(myPath)

    if my_file.is_file():
        return myPath

    else:
        LogMessage = f"Could not find file: {myPath}"
        Logger.exception(f"Error: {LogMessage}")
        return f"{RUNE_PATH}\\{RUNE_PLACEHOLDER}.png"


def get_champ_image_path(**kwargs):

    if "champ" in kwargs:
        champ = kwargs["champ"]

    else:
        LogMessage = f"No champ given"
        Logger.exception(f"Error: {LogMessage}")
        return f"{CHAMP_PATH}\\{CHAMP_PLACEHOLDER}.png"

    myPath = f"{CHAMP_PATH}\\{champ}.png"

    my_file = Path(myPath)

    if my_file.is_file():
        return myPath

    else:
        LogMessage = f"Could not find file: {myPath}"
        Logger.exception(f"Error: {LogMessage}")
        return f"{CHAMP_PATH}\\{CHAMP_PLACEHOLDER}.png"


def get_splash_image_path(**kwargs):

    if "champ" in kwargs:
        champ = kwargs["champ"]

    else:
        LogMessage = f"No champ given"
        Logger.exception(f"Error: {LogMessage}")
        return f"{SPLASH_PATH}\\{SPLASH_PLACEHOLDER}.png"

    myPath = f"{SPLASH_PATH}\\{champ}.png"

    my_file = Path(myPath)

    if my_file.is_file():
        return myPath

    else:
        LogMessage = f"Could not find file: {myPath}"
        Logger.exception(f"Error: {LogMessage}")
        return f"{SPLASH_PATH}\\{SPLASH_PLACEHOLDER}.png"


def get_summoner_image_path(**kwargs):

    if "spell" in kwargs:
        spell = kwargs["spell"]

    else:
        LogMessage = f"No spell given"
        Logger.exception(f"Error: {LogMessage}")
        return f"{SUMMONER_PATH}\\{SUMMONER_PLACEHOLDER}.png"

    myPath = f"{SUMMONER_PATH}\\{spell}.png"

    my_file = Path(myPath)

    if my_file.is_file():
        return myPath

    else:
        LogMessage = f"Could not find file: {myPath}"
        Logger.exception(f"Error: {LogMessage}")
        return f"{SUMMONER_PATH}\\{SUMMONER_PLACEHOLDER}.png"

    
def create_viz_message(**kwargs):

    """ returns a list of objects to be processed by viz widget
        in the form of [
            {
                "datapool_key": k,
                "datapool_value": v
            }
        ] 
    """

    return_list = []

    if "commands" in kwargs:

        for k, v in kwargs["commands"].items():

            return_list.append(
                {
                    "datapool_key": k,
                    "datapool_value": v
                }
            )
    
    return return_list

def sanitize_number(value):

    """ converts value to string and surrounds it with escaped double-double quotes
        (""VALUE"").  This allows sending numbers with commas to vizrt
    """

    return f'\"\"{value}\"\"'

#def two_line(value):
#    return value.replace(" ", "\r\n")

def two_line(value):
    return value


def get_passive_image(champ_name: str) -> str:
    return PASSIVES.get(champ_name.lower(), "_blank")
