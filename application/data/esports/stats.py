from kivy.logger import Logger


GOLD_DIFF_THRESHOLD = 100


    
def find_stat(key, stats):
    for this_stat in stats:
        if this_stat["name"] == key:
            return this_stat["value"]

    return None


def find_stats(key_list, stats):
    """
    Expects 'stats' from a livestats stats_update participant
    and a 'key_list' of the stats to search for
    returns dict if successful, None if none are found
    any key not found will have a value of None
    """
    return_dict = {}

    for thisKey in key_list:
        this_value = find_stat(thisKey, stats)

        if this_value is not None:
            return_dict[thisKey] = this_value

    if len(return_dict) > 0:
        return return_dict
    else:
        return None


def format_number(raw_number):

    """ Given a number returns the shortened string version
        in the format 18234 -> 18.2k 
        234 -> 234 """

    if -1000 < raw_number < 1000:
        return f"{abs(raw_number)}"
    else:
        return f"{abs(round(raw_number/1000, 1)):,.1f}k"


def format_signed_number(raw_number):

    """ Given a number returns the shortened string version
        in the format 18234 -> 18.2k 
        234 -> 234 """

    if -1000 < raw_number < 1000:

        if raw_number == 0:
            return f"{raw_number:}"

        else:
            return f"{raw_number:+}"

    else:
        return f"{round(raw_number/1000, 1):+,.1f}k"


def convert_milliseconds_to_HMS_string(milliseconds):

    """
    converts integer milliseconds into 
    HH:MM:SS string or MM:SS string
    """

    return_time = "00:00"
    negative_time = False

    if milliseconds < 0:
        negative_time = True 

    abs_milliseconds = abs(milliseconds)

    seconds = (abs_milliseconds//1000) % 60
    minutes = (abs_milliseconds//(1000*60)) % 60
    hours = (abs_milliseconds//(1000*60*60)) % 24

    if hours > 0:
        return_time = f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return_time = f"{minutes:01}:{seconds:02}"


    if negative_time:
        return f"-{return_time}"

    else:
        return return_time


def convert_MS_string_to_milliseconds(string_time):

    """assumes string_time has already been parsed into format MM:SS"""

    minutes, seconds = [int(x) for x in string_time.split(":")[:2]]
    
    milliseconds = (minutes * 60 * 1000) + seconds * 1000
    
    return milliseconds


def calculate_teams_damage(participants, *args):

    """
    returns list of TOTAL_DAMAGE_DEALT_TO_CHAMPIONS
    for all given participants
    """

    this_damage_list = []
    wanted_stats = ["TOTAL_DAMAGE_DEALT_TO_CHAMPIONS"]
        
    for this_participant in participants:

        if "stats" in this_participant:
            my_stat = find_stats(wanted_stats, this_participant["stats"])
            this_damage = round(my_stat["TOTAL_DAMAGE_DEALT_TO_CHAMPIONS"])
            this_damage_list.append(this_damage)

    if len(this_damage_list) > 0:
        return this_damage_list

    else:
        return None


def calculate_teams_damage_per_team(participants, *args):

    """
    Returns 2 lists of ints representing TOTAL_DAMAGE_DEALT_TO_CHAMPIONS
    One for team 100 and one for team 200
    """

    blue_damage = []
    blue_result = None
    red_damage = []
    red_result = None

    wanted_stats = ["TOTAL_DAMAGE_DEALT_TO_CHAMPIONS"]
        
    for this_participant in participants:

        if "stats" in this_participant:
            my_stat = find_stats(wanted_stats, this_participant["stats"])
            this_damage = round(my_stat["TOTAL_DAMAGE_DEALT_TO_CHAMPIONS"])
            
            if this_participant["teamID"] == 100:
                blue_damage.append(this_damage)
            elif this_participant["teamID"] == 200:
                red_damage.append(this_damage)

    if len(blue_damage) > 0:
        blue_result = blue_damage

    if len(red_damage) > 0:
        red_result = red_damage

    return blue_result, red_result


def calculate_sum_of_team_damage(participants, *args):
    """
    Sums TOTAL_DAMAGE_DEALT_TO_CHAMPIONS
    for all given participants, returns 2 values 
    one for team 100 and one for team 200
    """
    blue_damage = 0
    red_damage = 0

    for this_participant in participants:
        if "stats" in this_participant:
            dmg = find_stat("TOTAL_DAMAGE_DEALT_TO_CHAMPIONS", this_participant["stats"])
            
            if this_participant["teamID"] == 100:
                blue_damage += dmg
            elif this_participant["teamID"] == 200:
                red_damage += dmg

    return blue_damage, red_damage


def calculate_teams_gold(participants, *args):

    """
    Sums totalGold
    for all given participants
    returns a list of integers
    """

    this_gold_list = []
        
    for this_participant in participants:

        if "totalGold" in this_participant:
            this_gold_list.append(this_participant["totalGold"])

    if len(this_gold_list) > 0:
        return this_gold_list

    else:
        return None


def string_CS(participant, *args):

    result = ""

    value = calculate_CS(participant)

    if value is not None:
        result = f"{value:,d}"

    return result


def calculate_CS(participant, *args):

    """
    Given a participant, calculates Creep Score (CS) 
    from MINIONS_KILLED and NEUTRAL_MINIONS_KILLED
    returns integer or None if not found.
    """

    if "stats" not in participant:
        return None

    result = 0

    wanted_stats = [
        "MINIONS_KILLED",
        "NEUTRAL_MINIONS_KILLED"
    ]

    creep_score_dict = find_stats(wanted_stats, participant["stats"])

    minions = 0
    neutral_minions = 0

    if creep_score_dict is None:
        return None
    
    if creep_score_dict["MINIONS_KILLED"] is not None:
        minions = creep_score_dict["MINIONS_KILLED"]
    else:
        Logger.exception("Error: could not find data for MINIONS_KILLED in given stats")

    if creep_score_dict["NEUTRAL_MINIONS_KILLED"] is not None:
        neutral_minions = creep_score_dict["NEUTRAL_MINIONS_KILLED"]
    else:
        Logger.exception("Error: could not find data for NEUTRAL_MINIONS_KILLED in given stats")

    total_CS = minions + neutral_minions

    result = round(total_CS)

    return result


def string_CSD(player, opponent, *args):

    result = ""

    value = calculate_CSD(player, opponent)

    if value is not None:
        result = f"{value:+,d}"

    return result


def calculate_CSD(player, opponent, *args):

    """ given player and opponent (participants), 
        returns player_CS - opponentCS as an integer if successful
        returns None if data not found """

    result = None

    player_cs = calculate_CS(player)
    opponent_cs = calculate_CS(opponent)

    if (player_cs is not None and
        opponent_cs is not None
    ):
        result = player_cs - opponent_cs

    return result


def string_DMG(participant, *args):

    result = ""

    value = calculate_DMG(participant)

    if value is not None:
        result = f"{round(value):,d}"

    return result


def calculate_DMG(participant, *args):

    if "stats" not in participant:
        return None

    result = None

    wanted_stats = ["TOTAL_DAMAGE_DEALT_TO_CHAMPIONS"]

    damage = find_stats(wanted_stats, participant["stats"])

    if damage is not None:
        result = damage["TOTAL_DAMAGE_DEALT_TO_CHAMPIONS"]

    return result


def string_DMG_D(player, opponent, *args):

    result = ""

    value = calculate_DMG_D(player, opponent)

    if value is not None:
        result = f"{round(value):+,d}"

    return result


def calculate_DMG_D(player, opponent, *args):

    """ given player and opponent (participants), 
        returns player_DMG - opponent_DMG as an integer if successful
        returns None if data not found """

    if ("stats" not in player or
        "stats" not in opponent
    ):
        return None

    result = None

    player_dmg = calculate_DMG(player)
    opponent_dmg = calculate_DMG(opponent)

    if (player_dmg is not None and
        opponent_dmg is not None
    ):
        result = player_dmg - opponent_dmg

    return result


def calculate_DMG_percent(player, team_dmg, *args):
    """ Given a player and that players team damage, 
        return the percent of the teams damage coming from the player """
    dmg = find_stat("TOTAL_DAMAGE_DEALT_TO_CHAMPIONS", player["stats"])
    if team_dmg > 0:
        return dmg / team_dmg
    return 0


def string_DMG_percent(player, team_dmg, *args):
    value = calculate_DMG_percent(player, team_dmg)
    return f"{value:.1%}"


def calculate_total_gold(participant, *args):

    """ Given a participant, returns total gold
        as an integer.  Returns None if not found """

    if "totalGold" not in participant:
        return None

    return participant["totalGold"]


def calculate_current_gold(participant, *args):

    """ Given a participant, returns current gold
        as an integer.  Returns None if not found """

    if "currentGold" not in participant:
        return None

    return participant["currentGold"]


def string_GOLD(participant, *args):

    result = ""

    current_gold, total_gold = calculate_GOLD(participant)

    if (current_gold is not None and
        total_gold is not None    
    ):
        result = f"{current_gold:,d} ({total_gold:,d})"

    return result


def calculate_GOLD(participant, *args):

    """ Given a participant, returns current gold and total gold
        as integers.  Returns None, None if not found """

    current_gold = calculate_current_gold(participant)
    total_gold = calculate_total_gold(participant)

    return current_gold, total_gold


def string_GD(player, opponent, *args):

    result = ""

    value = calculate_GD(player, opponent)

    if value is not None:
        result = f"{value:+,d}"

    return result


def calculate_GD(player, opponent, *args):

    """ given player and opponent (participants), 
        returns player gold - opponent gold as an integer if successful
        returns None if data not found """

    result = None

    player_gold = calculate_total_gold(player)
    opponent_gold = calculate_total_gold(opponent)

    if (player_gold is not None and
        opponent_gold is not None
    ):
        result = player_gold - opponent_gold

    return result


def string_KDA(participant, *args):

    result = ""

    value = calculate_KDA(participant)

    if value is not None:
        result = value

    return result


def calculate_KDA(participant, *args):

    """ Given a participant, returns Kills/Deaths/Assists
        Returns None if not found"""

    if "stats" not in participant:
        return None

    result = None

    wanted_stats = [
        "CHAMPIONS_KILLED",
        "NUM_DEATHS",
        "ASSISTS"
    ]
    
    playerDict = find_stats(wanted_stats, participant["stats"])

    if playerDict is not None:

        kills = playerDict["CHAMPIONS_KILLED"]
        deaths = playerDict["NUM_DEATHS"]
        assists = playerDict["ASSISTS"]

        result = f"{kills}/{deaths}/{assists}"

    return result


def calculate_KP(participant, team_kills):

    if "stats" not in participant:
        return None

    if team_kills == 0:
        return 0

    result = None

    wanted_stats = [
        "CHAMPIONS_KILLED",
        "ASSISTS"
    ]

    playerDict = find_stats(wanted_stats, participant["stats"])

    if playerDict is not None:

        kills = playerDict["CHAMPIONS_KILLED"]
        assists = playerDict["ASSISTS"]

        result = (kills + assists) / team_kills

    return result


def string_KP(participant, team_kills):

    result = ""

    value = calculate_KP(participant, team_kills)

    if value is not None:
        result = f"{value:.1%}"

    return result


def string_LEVEL(participant, *args):

    result = ""

    value = calculate_LEVEL(participant)

    if value is not None:
        result = f"{value:,d}"

    return result


def calculate_LEVEL(participant, *args):

    """ Given a participant, returns level
        as an integer.  Returns None if not found """

    result = None

    if "level" in participant:
        result = participant["level"]

    return result


def string_VISION(participant, *args):

    result = ""

    value = int(calculate_vision(participant))

    if value is not None:
        result = f"{value:,d}"

    return result


def calculate_vision(participant, *args):

    if "stats" not in participant:
        return None

    result = None

    wanted_stats = ["VISION_SCORE"]

    vision_score_dict = find_stats(wanted_stats, participant["stats"])

    if vision_score_dict is not None:
        result = vision_score_dict["VISION_SCORE"]

    return result


def calculate_VSM(participant, game_time_ms, *args):
    """ Return vision score per minute for the given participant 
        Expected the participant and game_time in ms """
    vs = calculate_vision(participant)
    minutes = game_time_ms / 60000
    if minutes > 0:
        return vs / minutes
    return 0


def string_VSM(participant, game_time_ms, *args):
    value = calculate_VSM(participant, game_time_ms)
    return f"{value:.2f}"


def calculate_XP(participant, *args):

    """ Given a participant, returns XP
        as an integer.  Returns None if not found """

    result = None

    if "XP" in participant:
        result = participant["XP"]

    return result


def string_XPD(player, opponent, *args):

    result = ""

    value = calculate_XPD(player, opponent)

    if value is not None:
        result = f"{value:+,d}"

    return result


def calculate_XPD(player, opponent, *args):

    """ given player and opponent (participants), 
        returns player XP - opponent XP as an integer if successful
        returns None if data not found """

    result = None

    player_XP = calculate_XP(player)
    opponent_XP = calculate_XP(opponent)

    if (player_XP is not None and
        opponent_XP is not None
    ):
        result = player_XP - opponent_XP

    return result


def calculate_objective_damage(participant, *args):

    if "stats" not in participant:
        return None

    result = None

    wanted_stats = ["TOTAL_DAMAGE_DEALT_TO_OBJECTIVES"]

    damage_dict = find_stats(wanted_stats, participant["stats"])

    if damage_dict is not None:
        result = damage_dict["TOTAL_DAMAGE_DEALT_TO_OBJECTIVES"]

    return result


def default(*args):
    return None


def string_default(*args):
    return ""


STAT_MAP = {
    "K/D/A": calculate_KDA,
    "CS": calculate_CS,
    "CSD": calculate_CSD,
    "GD": calculate_GD,
    "DMG": calculate_DMG,
    "GOLD": calculate_GOLD,
    "DMG-D": calculate_DMG_D,
    "LEVEL": calculate_LEVEL,
    "XPD": calculate_XPD,
    "VS": calculate_vision,
    "": default
}

STRING_STAT_MAP = {
    "K/D/A": string_KDA,
    "CS": string_CS,
    "CSD": string_CSD,
    "GD": string_GD,
    "DMG": string_DMG,
    "GOLD": string_GOLD,
    "DMG-D": string_DMG_D,
    "LEVEL": string_LEVEL,
    "XPD": string_XPD,
    "VS": string_VISION,
    "": string_default
}

def get_participant(participants: list[dict], id: int) -> dict:

    result = {}

    for this_participant in participants:
        if ("participantID" in this_participant and
            this_participant["participantID"] == id
        ):
            result = this_participant

    return result

def get_DMG_pct(participants: list[dict], id: int) -> float:

    my_data = get_participant(participants, id)

    dmg = calculate_DMG(my_data)

    sum = 0
    start, end = 1, 5

    if id > 5:
        start, end = 6, 10

    for this_participant in participants:
        if ("participantID" in this_participant and
            start <= this_participant["participantID"] <= end
        ):
            sum += calculate_DMG(this_participant)

    if sum > 0:
        return dmg/sum
    else:
        return 0
    
def string_dmg_pct(participants: list[dict], id: int) -> str:

    value = get_DMG_pct(participants, id)
    return f"{value:.1%}"
