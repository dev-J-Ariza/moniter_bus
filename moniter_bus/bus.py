from moniter_bus import api


def get_station(bus_line):
    return api.get_station(bus_line)


def get_all_buses():
    return api.get_all_busses()


def print_help():
    return api.print_help()
