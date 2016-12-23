import tempfile
import datetime
from nose.tools import assert_raises
from traffic_mon import TrafficMon, NotEnoughDataPoints, STATUS


LOG_DATA = """231.47.140.70 user-identifier frank [22/Dec/2016:18:19:57 +0100] "GET /bar/create HTTP/1.0" 200 1027
245.44.172.53 user-identifier alice [22/Dec/2016:18:19:57 +0100] "GET /pages/create HTTP/1.0" 502 1928
199.177.67.46 user-identifier frank [22/Dec/2016:18:19:58 +0100] "GET /posts/foo?appID=xxxx HTTP/1.0" 200 1997
199.177.67.46 user-identifier frank [22/Dec/2016:18:19:59 +0100] "GET /posts/foo/bar?appID=xxxx HTTP/1.0" 200 1997
199.177.67.46 user-identifier frank [22/Dec/2016:18:20:01 +0100] "GET / HTTP/1.0" 200 1997
199.177.67.46 user-identifier frank [22/Dec/2016:18:20:01 +0100] "GET /posts/foo?appID=xxxx HTTP/1.0" 200 1997
199.177.67.46 user-identifier frank [22/Dec/2016:18:20:01 +0100] "GET /posts/foo/bar?appID=xxxx HTTP/1.0" 200 1997
199.177.67.46 user-identifier frank [22/Dec/2016:18:20:02 +0100] "GET / HTTP/1.0" 200 1997
199.177.67.46 user-identifier frank [22/Dec/2016:18:22:03 +0100] "GET /posts/foo?appID=xxxx HTTP/1.0" 200 1997
199.177.67.46 user-identifier frank [22/Dec/2016:18:22:04 +0100] "GET /posts/foo/bar?appID=xxxx HTTP/1.0" 200 1997
199.177.67.46 user-identifier frank [22/Dec/2016:18:22:04 +0100] "GET / HTTP/1.0" 200 1997
"""

# TODO: Add more tests for different section parsing and malformed log handling


def test_traffic_no_alert():
    with tempfile.NamedTemporaryFile(mode="w+") as temp:
        temp.write(LOG_DATA)
        temp.flush()

        # 1 second window, wait for 3 seconds of
        # data before alerting

        traffic_mon = TrafficMon(logfile=temp.name, num_ticks=3, tick_window=1)
        ts = datetime.datetime.strptime("22/Dec/2016:18:22:06 +0100", '%d/%b/%Y:%H:%M:%S %z')
        one_sec = datetime.timedelta(seconds=1)

        # The first two ticks will not have enough
        # datapoints

        with assert_raises(NotEnoughDataPoints):
            traffic_mon.tick(tick_start=ts)
            ts += one_sec
            traffic_mon.check_alert(1)
        with assert_raises(NotEnoughDataPoints):
            traffic_mon.tick(tick_start=ts)
            ts += one_sec
            traffic_mon.check_alert(1)
        # No log entries will be in the window
        # so there will not be any alerts
        traffic_mon.tick(tick_start=ts)
        assert traffic_mon.check_alert(1) == (None, None)


def test_traffic_alert():
    with tempfile.NamedTemporaryFile(mode="w+") as temp:
        temp.write(LOG_DATA)
        temp.flush()

        # 1 second window, wait for 3 seconds of
        # data before alerting

        traffic_mon = TrafficMon(logfile=temp.name, num_ticks=3, tick_window=1)
        ts = datetime.datetime.strptime("22/Dec/2016:18:22:04 +0100", '%d/%b/%Y:%H:%M:%S %z')
        one_sec = datetime.timedelta(seconds=1)

        # The first two ticks will not have enough
        # datapoints

        traffic_mon.tick(tick_start=ts)
        ts += one_sec
        traffic_mon.tick(tick_start=ts)
        ts += one_sec
        traffic_mon.tick(tick_start=ts)

        assert list(traffic_mon._queue) == [3, 2, 0]
        # Above the average, no alert
        assert traffic_mon.check_alert(1.7) == (None, None)
        # Below the averge, alert
        assert traffic_mon.check_alert(1.5)[0] == STATUS.alert


def test_traffic_alert_clear():
    with tempfile.NamedTemporaryFile(mode="w+") as temp:
        temp.write(LOG_DATA)
        temp.flush()

        # 1 second window, wait for 3 seconds of
        # data before alerting

        traffic_mon = TrafficMon(logfile=temp.name, num_ticks=3, tick_window=1)
        ts = datetime.datetime.strptime("22/Dec/2016:18:22:04 +0100", '%d/%b/%Y:%H:%M:%S %z')
        one_sec = datetime.timedelta(seconds=1)

        # The first two ticks will not have enough
        # datapoints

        traffic_mon.tick(tick_start=ts)
        ts += one_sec
        traffic_mon.tick(tick_start=ts)
        ts += one_sec
        traffic_mon.tick(tick_start=ts)

        assert list(traffic_mon._queue) == [3, 2, 0]
        # Average of [3, 2, 0] will be above the threshold
        # of 1.5, alert
        assert traffic_mon.check_alert(1.5)[0] == STATUS.alert
        ts += one_sec
        traffic_mon.tick(tick_start=ts)

        # Average of [2, 0, 0] willb e below the threshold
        # of 1.5, clear
        assert list(traffic_mon._queue) == [2, 0, 0]
        assert traffic_mon.check_alert(1.5)[0] == STATUS.clear
        ts += one_sec
        traffic_mon.tick(tick_start=ts)

        # Once we clear we should not clear again
        assert list(traffic_mon._queue) == [0, 0, 0]
        assert traffic_mon.check_alert(1.5) == (None, None)
