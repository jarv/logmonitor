from logreader import LogReader
import tempfile

LOG_DATA = """231.47.140.70 user-identifier frank [22/Dec/2016:18:19:57 +0100] "GET /bar/create HTTP/1.0" 200 1027
245.44.172.53 user-identifier alice [22/Dec/2016:18:20:32 +0100] "GET /pages/create HTTP/1.0" 502 1928
199.177.67.46 user-identifier frank [22/Dec/2016:18:21:10 +0100] "GET /posts/foo?appID=xxxx HTTP/1.0" 200 1997
208.186.41.33 user-identifier mike [22/Dec/2016:18:22:37 +0100] "DELETE /posts/1/display HTTP/1.0" 200 2149
68.9.160.181 user-identifier bob [22/Dec/2016:18:23:07 +0100] "PUT /posts/1/display HTTP/1.0" 200 2504
17.7.242.54 user-identifier frank [22/Dec/2016:18:26:57 +0100] "GET /posts/foo?appID=xxxx HTTP/1.0" 200 1190
238.251.162.163 user-identifier alice [22/Dec/2016:18:30:37 +0100] "GET /posts/1/display HTTP/1.0" 404 3357"""

LOG_LINE = """56.12.143.95 user-identifier alice [22/Dec/2016:18:22:01 +0100] "GET /posts/1/display HTTP/1.0" 404 1745"""


def test_get_lines_from_log():
    with tempfile.NamedTemporaryFile(mode="w+") as temp:
        temp.write(LOG_DATA)
        temp.flush()
        l = LogReader(temp.name)
        lines = list(l.get_lines_from_log())
        assert [line.rstrip() for line in lines] == LOG_DATA.split("\n")
        # No more lines are returned when we are at
        # the end of the file.
        more_lines = list(l.get_lines_from_log())
        assert not more_lines
        # Add one more line and confirm we get it back
        temp.write(LOG_LINE)
        temp.flush()
        lines = list(l.get_lines_from_log())
        assert [line.rstrip() for line in lines] == LOG_LINE.split("\n")
