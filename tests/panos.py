import requests
import time
headers= {'Content-type': 'application/json'}
while True:
    requests.packages.urllib3.disable_warnings()
    try:
        receive = requests.get("https://127.0.0.1:2999/replay/playback", verify=False)
    except requests.RequestException as e:
        print "cannot see game"
        pass
    else:
        print receive.content
        try:
            send = requests.post("https://delay.stats.ber1.esportstech.riotgames.com/delay" , data=receive.content, verify=False, headers=headers)
        except requests.RequestException as e:
            print "cannot see Eike"
            print e
            pass
        else:
            print send.content