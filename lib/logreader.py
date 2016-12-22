from os.path import exists


class LogParseError(Exception):
    pass


class LogNotFoundError(Exception):
    pass


class LogReader(object):

    def __init__(self, logfile):
        self._last_position = 0
        self._logfile = logfile

    def get_lines_from_log(self, bufsize=4096):
        """
        Gets lines from the log, remembers
        the file position so it does not read
        the entire log on every call.
        """
        fname = self._logfile
        if not exists(fname):
            raise LogNotFoundError("Logfile {} not found".format(fname))
        with open(fname, 'r') as f:
            if self._last_position:
                f.seek(self._last_position)
            for line in f:
                yield line
            self._last_position = f.tell()
