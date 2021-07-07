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
REAL_TIME_URL = 'http://www.bjbus.com/api/api_etaline_list.php'
STATION_URL = 'http://www.bjbus.com/api/api_etastation.php'

token = "eyJhbGciOiJIUzI1NiIsIlR5cGUiOiJKd3QiLCJ0eXAiOiJKV1QifQ.eyJwYXNzd29yZCI6IjY0ODU5MTQzNSIsInVzZXJOYW1lIjoiY" \
    "mpidXMiLCJleHAiOjE2MjcwOTkyMDB9.OQYkF6rC9jfgxoC5nXDjjv1nqDIv3KfXqol0ATdts9g"
direction_name = ''


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

    line_ids = None
    line_names = None
    if read_from_cache:
        print('Getting from cache')
        line_ids = cache_data['line_ids']
        line_names = cache_data['line_names']
    else:
        print('Getting from web')
        play_load = {'what': str(bus_line)}
        r = requests.get(REAL_TIME_URL, params=play_load)
        response = json.loads(r.content.decode(encoding='utf-8'))
        data_list = response['response']['resultset']['data']['feature']
        line_ids = [data_list[0]['lineId'], data_list[1]['lineId']]
        line_names = [data_list[0]['firstStationName'] + '-' + data_list[0]['lastStationName'],
                      data_list[1]['firstStationName'] + '-' + data_list[1]['lastStationName']]

    print('Please input direction:' + '\n' + Fore.CYAN + '1 ' + Fore.RESET + 'for ' + line_names[0] + '\n'
          + Fore.CYAN + '2 ' + Fore.RESET + 'for ' + line_names[1])
    input_direction = int(input()) - 1
    direction = line_ids[input_direction]
    global direction_name
    direction_name = '%s(%s)' % (str(bus_line), line_names[input_direction])
    print(direction_name)

    if read_from_cache and direction in cache_data['data']:
        print('Getting from cache')
        res = cache_data['data'][direction]
    else:
        print('Getting from web')
        play_load = {'lineId': direction, 'token': token}
        r = requests.get(STATION_URL, params=play_load)
        response = json.loads(r.content.decode(encoding='utf-8'))
        res = response['data']
        # update
        station_data = {}
        if cache_data and cache_data['data']:
            station_data = cache_data['data']
        station_data[direction] = res
        tmp = {
            'time': time.time(),
            'line_ids': line_ids,
            'line_names': line_names,
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
        print(Fore.CYAN + station['stopNumber'] + "\t" + Fore.RESET + station['stopName'])
    return res
