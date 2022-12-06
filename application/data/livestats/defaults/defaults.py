import json
from pathlib import Path
from datetime import datetime, timezone

def get_default_data(file_name):

    data_path = Path().joinpath("data", "livestats", "defaults", file_name)

    with data_path.open() as f:
        data_string = f.read()

    return json.loads(data_string)


DEFAULT_GAME_INFO = get_default_data("game_info.json")
DEFAULT_STATS_UPDATE = get_default_data("stats_update.json")


def get_default_game_info():
    
    new_game_info = DEFAULT_GAME_INFO
    new_game_info["rfc460Timestamp"] = datetime.now(tz=timezone.utc).isoformat()

    return new_game_info


def get_default_stats_update():
    
    new_stats_update = DEFAULT_STATS_UPDATE
    new_stats_update["rfc460Timestamp"] = datetime.now(tz=timezone.utc).isoformat()

    return new_stats_update

