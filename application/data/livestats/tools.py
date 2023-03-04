from kivy.logger import Logger

def format_player_attribute(key, value):

    """ Given an attribute key and value from participant,
        returns the proper key suffix and formatted variable
        Returns None, None if unsuccessfull """

    pass



def parse_name(name: str) -> tuple[str, str]:

    """Given name as a String, 
    returns 3 letter-tricode and a Player Name
    
    returns empty string and name if it can't find tricode

    """

    tricode = ""
    player_name = name

    name_array = name.split(" ")

    if len(name_array) > 1:
        tricode = name_array[0]
        player_name = " ".join(name_array[1:])

    return tricode, player_name
