import requests
import time
import json

HEADERS= {'Content-type': 'application/json'}

time_server_session = requests.Session()

this_time = 0.0
pause_time = 0.2

game_time = {
    "length": 0.0,
    "paused": False,
    "seeking": False,
    "speed": 1.0,
    "time": 0.0
}

while True:
    
    requests.packages.urllib3.disable_warnings()

    game_time["time"] = this_time

    body = json.dumps(game_time)
    
    try:
        with time_server_session as ts:
            send = ts.post("http://44.231.66.109:8080/observer-time" , data=body, verify=False, headers=HEADERS)
    
    except Exception as e:
        print(e)

    else:

        this_time += pause_time
        time.sleep(pause_time)

        print(game_time)