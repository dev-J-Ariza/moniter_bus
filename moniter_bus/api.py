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
    db_path = os.path.join(os.path.dirname(__file__), 'db', 'all_station.txt')
    cache_data = {}
    read_from_cache = False
    with open(db_path, 'r', encoding='utf-8') as f:
        try:
            db_data = json.loads(f.read())
            cache_data = db_data.get(str(bus_line))
            if cache_data and time.time() - cache_data['time'] <= 24 * 3600:
                read_from_cache = True
        except json.JSONDecodeError as e:
            pass

    dir_codes = None
    dir_names = None
    play_load = play_load = {'act': 'getLineDir', 'selBLine': str(bus_line)}
    if read_from_cache:
        print('Getting from cache')
        dir_codes = cache_data['dir_codes']
        dir_names = cache_data['dir_names']
    else:
        print('Getting from web')
        r = requests.get(MAIN_URL2, params=play_load)
        response = r.content.decode(encoding='utf-8')
        dir_codes = re.findall('data-uuid="(\\d+)"', response)
        dir_names = re.findall('>(.*?)</a>', response)

    print('Please input direction:' + '\n' + Fore.CYAN + '1 ' + Fore.RESET + 'for ' + dir_names[0] + '\n'
          + Fore.CYAN + '2 ' + Fore.RESET + 'for ' + dir_names[1])
    direction = dir_codes[int(input()) - 1]

    if read_from_cache and direction in cache_data['data']:
        print('Getting from cache')
        res = cache_data['data'][direction]
    else:
        print('Getting from web')
        play_load['act'] = 'getDirStation'
        play_load['selBDir'] = direction
        r = requests.get(MAIN_URL2, params=play_load)
        response = r.content.decode(encoding='utf-8')
        res = re.findall('<a href="javascript:;" data-seq="(\\d+)">(.*?)</a>', response)
        # update
        station_data = {}
        if cache_data and cache_data['data']:
            station_data = cache_data['data']
        station_data[direction] = res
        tmp = {
            'time': time.time(),
            'dir_codes': dir_codes,
            'dir_names': dir_names,
            'data': station_data
        }
        with open(db_path, 'r+', encoding='utf-8') as f:
            try:
                db_data[str(bus_line)] = tmp
                f.write(json.dumps(db_data, ensure_ascii=False, indent=4))
            except json.JSONDecodeError as e:
                pass

    print(' --------------------------------')
    for station in res:
        print(Fore.CYAN + station[0] + "\t" + Fore.RESET + station[1])
