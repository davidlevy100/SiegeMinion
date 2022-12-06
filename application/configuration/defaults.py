import json
from pathlib import Path

def get_defaults():

    """Returns a dict of the application default settings"""

    path = Path.cwd().joinpath('configuration', 'defaults.json')

    with path.open(mode='r') as f:
        defaults = json.load(f)

    return defaults
