import re
from config import config_from_yaml
from collections import Counter, defaultdict
from logreader import LogReader

class LogParseError(Exception):
    pass


class LogStats(object):

    def __init__(self):
        self._stats = defaultdict(Counter)
        self._last_position = None
        self._config = config_from_yaml()
        self._l = LogReader()

    def get_stats(self):
        """
        Returns a dictionary of updated statistics
        for the configured log containing cumalative
        stats.
        """
        for line in self._l.get_lines_from_log():
            # TODO Improve the regex to make it more robust
            m = re.search(r' "(?P<verb>.*?) (?P<section>.*?) .*?" (?P<status>.*?) (?P<size>.*?)$', line)
            if not m:
                raise LogParseError("Unable to find section in line '{}'".format(line))
            for stat in self._config['stats']:
                self._stats[stat][m.group(stat)] += 1
        return self._stats
