#!/usr/bin/env python
import argparse
import urllib3

from time import sleep
import json
from pathlib import Path

import re
import subprocess
from urllib.parse import urlencode
from base64 import urlsafe_b64encode
from datetime import datetime
from pathlib import Path
import json

from requests import Session
from sortedcontainers import SortedDict

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HISTORY_FOLDER = Path("history")

class LeagueNotRunningException(Exception):
    """ Exception Raised if the 
        League Client is not running """

    def __str__(self):
        return "LOL Champ Select Client not found in running processes"


class ChampSelect:

    def get_process(self):
        """ Checks if the League Client is running
        The function determines whether the client is running and returns a string
        containing the commandline arguments that were passed when the client was
        being launched.
        Returns:
            A string (the string is empty if the client isn't running)
        """

        # Using the WMIC command to retrieve running processes.
        cmd = 'WMIC PROCESS get Caption,Commandline'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

        result = ''

        for line in proc.stdout:
            line = line.decode('utf-8')

            if 'LeagueClientUx.exe' in line:
                # Formatting the string for easier processing
                result = re.sub(' +', ' ', line).rstrip()
                break

        return result


    def get_connection_details(self):
        """ Retrieves the info required to connect to the LCU Api
        The function returns the port and the authentication token that the League
        client that is currently running is using for its api
        Returns:
            A tuple containing the token(string) and the port(string)
        """

        command_line = self.get_process()

        if command_line == '':
            raise LeagueNotRunningException

        token = re.search(r'\"--remoting-auth-token=(\S+)\"',
                        command_line).group(1)
        port = re.search(r'\"--app-port=(\S+)\"', command_line).group(1)

        return (token, port)


    def construct_request(self):

        token, port = self.get_connection_details()

        hash_string = urlsafe_b64encode(f"riot:{token}".encode('utf-8')).decode('utf-8')

        headers = {
            "Authorization": f"Basic {hash_string}",
            'Accept': "application/json",
            'Cache-Control': "no-cache",
            'Host': f"127.0.0.1:{port}",
            'accept-encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

        full_url = f"https://127.0.0.1:{port}/lol-champ-select/v1/session"


        return headers, full_url


    def get_data(self):

        headers, url = self.construct_request()

        this_session = Session()

        cs_running = True

        data = SortedDict()

        while cs_running:

            try:

                response = this_session.get(url, headers=headers, verify=False)

                if response.status_code == 200:
                    this_value = response.json()

                    if ("timer" in this_value and
                        "internalNowInEpochMs" in this_value["timer"]
                    ):
                        this_key = this_value["timer"]["internalNowInEpochMs"]
                
                        if this_key not in data:

                            print(f"Storing event {this_key}")
                            data[this_key] = this_value
                
                sleep(0.5)

            except KeyboardInterrupt:
                cs_running = False

        print("\nWriting files, please wait")

        folder = HISTORY_FOLDER.joinpath(
            f"champ_select_{datetime.now().strftime('%b_%d_%H_%M_%S')}"
        )

        folder.mkdir(exist_ok=True, parents=True)

        for key, value in data.items():

            my_file = folder.joinpath(f"{key}.json")

            my_file.write_text(
                json.dumps(
                    value, 
                    indent=4, 
                    sort_keys=True
                )
            )






class DevChampSelect(ChampSelect):

    def get_connection_details(self):
        return ("developer", 9090)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--dev", help="use this when you start league in dev mode with these flags:  --remoting-auth-token=developer --app-port=9090")

    args = parser.parse_args()

    if args.dev:
        CS = DevChampSelect()
    else:
        CS = ChampSelect()
    
    CS.get_data()
