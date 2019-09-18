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


class LoggerPathException(Exception):
    def __init__(self, path):
        if path is None:
            self.message = 'The input path is None'
        else:
            self.message = 'The input path {} is not valid'.format(path)

    def __str__(self):
        return self.message
