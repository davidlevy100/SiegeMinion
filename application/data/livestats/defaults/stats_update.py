import json
from pathlib import Path

def get_default_stats_update():

    path = Path.cwd().joinpath('data', 'livestats','defaults','stats_update.json')

    with path.open(mode='r') as f:
        stats_update = json.load(f)

    return stats_update