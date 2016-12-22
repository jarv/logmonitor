from config import config_from_yaml


class LogReader(object):

    def __init__(self):
        self._last_position = 0
        self._config = config_from_yaml()

    def get_lines_from_log(self):
        """
        Gets lines from the log, remembers
        the file position so it does not read
        the entire log on every call.
        """
        fname = self._config['log']
        with open(fname, 'r') as f:
            if self._last_position:
                f.seek(self._last_position)
            for line in f:
                yield line
            self._last_position = f.tell() + 1
