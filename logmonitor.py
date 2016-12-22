#!/usr/bin/env python3

import time
import sys
import os
from tabulate import tabulate
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
from config import config_from_yaml  # noqa: E731
from logstats import LogStats  # noqa: E731


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


def disp_min(stats):
    min_stats = []
    for stat in config['stats']:
        min_stats.append((stat, min(stats[stat].items(), key=lambda k: k[1])))
    print(tabulate(min_stats, headers=["Minimum Name", "Name, Count"]))


def disp_max(stats):
    max_stats = []
    for stat in config['stats']:
        max_stats.append((stat, max(stats[stat].items(), key=lambda k: k[1])))
    print(tabulate(max_stats, headers=["Maximum Name", "Name, Count"]))


def every_five():
    disp_min(stats.get_stats())
    print()
    disp_max(stats.get_stats())


def every_ten():
    print("{} Every 10".format(time.strftime('%a %H:%M:%S')))


if __name__ == '__main__':

    sys.stdout = Unbuffered(sys.stdout)
    config = config_from_yaml()
    stats = LogStats()
    counter = 0
    while True:
        if counter % 5 == 0:
            every_five()
        if counter % 10 == 0:
            every_ten()
        time.sleep(1)
        counter += 1
