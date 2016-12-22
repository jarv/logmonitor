from logreader import LogReader, LogParseError
import datetime
import pytz
import re
from collections import deque


class NotEnoughDataPoints(Exception):
    pass


class STATUS:
    alert = "alert"
    clear = "clear"


class TrafficMon(object):
    def __init__(self, logfile, num_ticks=120, tick_window=1):
        self._num_ticks = num_ticks
        self._tick_window = tick_window  # seconds
        self._buffer = []
        self._logreader = LogReader(logfile)
        self._queue = deque([], num_ticks)
        self._status = None

    def check_alert(self, threshold):
        avg = self._get_avg()
        if avg >= threshold:
            self._status = STATUS.alert
            return STATUS.alert, avg
        if self._status == STATUS.alert and avg < threshold:
            self._status = STATUS.clear
            return STATUS.clear, avg
        return None, None

    def _get_avg(self):
        if len(self._queue) < self._num_ticks:
            raise NotEnoughDataPoints("Waiting for more datapoints: have: {}, need: {}".format(len(self._queue), self._num_ticks))
        return float(sum(self._queue) / max(len(self._queue), 1))

    def tick(self, tick_start=None):
        """
        This function should be called once for every tick window.

        Read up to the end of the file we are monitoring
        keeping entries in the buffer for current_time - tick_window.

        TODO: * Add alert dimensions for different traffic patterns,
                GETS, POSTS, 500s, p50, p90 etc.
              * Categories of alerts, severities.
              * Low traffic as well as high traffic.
        """

        if not tick_start:
            # current time, timezone aware
            tick_start = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        increment = datetime.timedelta(seconds=self._tick_window)
        keep = tick_start - increment

        # Remove entries in buffer that are older
        # than the keep window
        self._buffer = [line for line in self._buffer if not self._discard_line(line, keep)]

        # Read up until the end of the logfile, add
        # entries that are in the keep window
        for line in self._logreader.get_lines_from_log():
            if self._discard_line(line, keep):
                continue
            self._buffer.append(line)
        self._queue.append(len(self._buffer))

    def _discard_line(self, line, keep):
        """
        Returns true if the line should be
        discarded because it is older than
        the keep window.
        """
        m = re.search(r' \[(?P<datetime>.*?)\] ', line)
        if not m:
            raise LogParseError("Unable to find date timestamp in line '{}'".format(line))
        ts = datetime.datetime.strptime(m.group('datetime'), '%d/%b/%Y:%H:%M:%S %z')
        if ts < keep:
            return True
        else:
            return False
