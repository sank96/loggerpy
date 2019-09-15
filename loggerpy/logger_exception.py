class LoggerNameException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class LoggerLevelException(Exception):
    def __init__(self, level):
        self.message = 'No level \'{}\' found.'.format(level.upper())

    def __str__(self):
        return self.message
