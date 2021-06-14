"""
Usage:
    bus.get_station(bus_line)
    bus.print_help()
Example:
    bus.get_station(438)         Show stations, directions and positions of bus 438
"""

import json
import time

import requests
import re
import os
from colorama import Fore

MAIN_URL1 = 'http://www.bjbus.com/home/index.php'
MAIN_URL2 = 'http://www.bjbus.com/home/ajax_rtbus_data.php'


def print_help():
    print(' ------- ' + Fore.CYAN + 'BeiJing Real Bus' + Fore.RESET + ' -------')
    print('|                                 |')
    print('|      Github: dev-J-Ariza        |')
    print('|   project: ' + Fore.BLUE + 'moniter_bus' + Fore.RESET + '          |')
    print(' --------------------------------')
    print(__doc__)


def get_all_busses():
    db_path = os.path.join(os.path.dirname(__file__), 'db', 'all_bus.txt')
    with open(db_path, 'r') as f:
        try:
            db_data = json.loads(f.read())
            if time.time() - db_data['time'] <= 24 * 3600:
                print('Getting from cache')
                return db_data['data']
        except json.JSONDecodeError as e:
            pass

    print('Getting from Web')
    r = requests.get(MAIN_URL1)
    res = re.findall('<a href="javascript:;">(\\d+)</a>', r.content.decode(encoding='utf-8'))
    db_data = {
        'time': time.time(),
        'data': res,
    }
    with open(db_path, 'w+') as f:
        f.write(json.dumps(db_data, ensure_ascii=False, indent=4))
    return res


def get_station(bus_line):
    payload = {'act': 'getLineDir', 'selBLine': str(bus_line)}
    r = requests.get(MAIN_URL2, params=payload)
    response = r.content.decode(encoding='utf-8')
    dir_codes = re.findall('data-uuid="(\\d+)"', response)
    dir_names = re.findall('>(.*?)</a>', response)
    print('Please input direction:' + '\n' + Fore.CYAN + '1 ' + Fore.RESET + 'for ' + dir_names[0] + '\n'
          + Fore.CYAN + '2 ' + Fore.RESET + 'for ' + dir_names[1])
    direction = dir_codes[int(input()) - 1]

    payload['act'] = 'getDirStation'
    payload['selBDir'] = direction
    r = requests.get(MAIN_URL2, params=payload)
    response = r.content.decode(encoding='utf-8')
    res = re.findall('<a href="javascript:;" data-seq="(\\d+)">(.*?)</a>', response)
    print(' --------------------------------')
    for station in res:
        print(Fore.CYAN + station[0] + "\t" + Fore.RESET + station[1])
