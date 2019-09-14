class LoggerNameException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class LoggerLevelExcepiton(Exception):
    def __init__(self, level, l):
        self.message = 'No level \'{}\' found. Possible levels {}'.format(level.upper(), l)

    def __str__(self):
        return self.message
