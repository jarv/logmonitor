import re
from collections import Counter, defaultdict
from logreader import LogReader, LogParseError


class LogStats(object):

    def __init__(self, logfile, stats):
        self._stats = stats
        self._stats_summary = defaultdict(Counter)
        self._last_position = None
        self._logreader = LogReader(logfile)

    def get_summary_stats(self):
        """
        Returns a dictionary of updated statistics
        for the configured log containing cumalative
        stats.
        TODO: * Improve the regex to make it more robust
        """
        for line in self._logreader.get_lines_from_log():
            m = re.search(r' "(?P<verb>.*?) (?P<section>.*?) .*?" (?P<status>.*?) (?P<size>.*?)$', line)
            if not m:
                raise LogParseError("Unable to find section in line '{}'".format(line))
            for stat in self._stats:
                self._stats_summary[stat][m.group(stat)] += 1
        return self._stats_summary
