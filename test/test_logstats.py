from logstats import LogStats
from collections import Counter
import tempfile


LOG_DATA = """231.47.140.70 user-identifier frank [22/Dec/2016:18:19:57 +0100] "GET /bar/create HTTP/1.0" 200 1027
245.44.172.53 user-identifier alice [22/Dec/2016:18:20:32 +0100] "GET /pages/create HTTP/1.0" 502 1928
199.177.67.46 user-identifier frank [22/Dec/2016:18:21:10 +0100] "GET /posts/foo?appID=xxxx HTTP/1.0" 200 1997
199.177.67.46 user-identifier frank [22/Dec/2016:18:21:10 +0100] "GET /posts/foo/bar?appID=xxxx HTTP/1.0" 200 1997
199.177.67.46 user-identifier frank [22/Dec/2016:18:21:10 +0100] "GET / HTTP/1.0" 200 1997"""

# TODO: Add more tests for different section parsing and malformed log handling

def test_get_lines_from_log():
    with tempfile.NamedTemporaryFile(mode="w+") as temp:
        temp.write(LOG_DATA)
        temp.flush()
        l = LogStats(temp.name, ["section"])
        expected_counts = Counter({"/bar": 1, "/pages": 1, "/posts": 2, "/": 1})
        assert l.get_summary_stats()["section"] == expected_counts
