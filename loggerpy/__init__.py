import os
from datetime import datetime

from loggerpy.logger_exception import LoggerNameException, LoggerLevelExcepiton
from loggerpy.colors import colors


class Level:
    NO_LOGGER = 'NO LOGGER'
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class _Level:
    """
    This class represents the possible levels of the logger.
    ...
    Attributes
    ----------
    DEBUG: dict
        The lowest priority level. Usually it is not contained into saved log, but it is only used in coding.
        Default color blue.
    INFO: dict
        It is usually used to show some information, e.g. after a computation
        Default color green.
    WARNING: dict
        It is used to represent something that is not going as planned, but it not broke the execution of program.
        Default color yellow.
    ERROR: dict
        It represents the error that blocks the execution of the script.
        Default color red
    CRITICAL: dict
        It represent a very important error that must be fix ASAP.
        Default color black with a red background.
    NO_LOGGER: dict
        It is the level that not print or save the log.
        It is usually used when the developer wants only save or print the logs.

    Methods
    -------
    """

    #TODO dare la possibilità di modificare i colori

    NO_LOGGER = {'color': colors.get_color(), 'name': Level.NO_LOGGER,
                 'level': 5}
    DEBUG = {'color': colors.get_color(fg=colors.fg.blue), 'name': Level.DEBUG,
             'level': 0}
    INFO = {'color': colors.get_color(fg=colors.fg.lightgreen), 'name': Level.INFO,
            'level': 1}
    WARNING = {'color': colors.get_color(fg=colors.fg.yellow, type=colors.bold), 'name': Level.WARNING,
               'level': 2}
    ERROR = {'color': colors.get_color(fg=colors.fg.red), 'name': Level.ERROR,
             'level': 3}
    CRITICAL = {'color': colors.get_color(bg=colors.bg.red), 'name': Level.CRITICAL,
                'level': 4}

    @staticmethod
    def find_level(level):
        if level is None:
            raise LoggerLevelExcepiton('NONE')

        level = level.upper()

        if level == _Level.NO_LOGGER['name']:
            return _Level.NO_LOGGER
        elif level == _Level.DEBUG['name']:
            return _Level.DEBUG
        elif level == _Level.INFO['name']:
            return _Level.INFO
        elif level == _Level.WARNING['name']:
            return _Level.WARNING
        elif level == _Level.ERROR['name']:
            return _Level.ERROR
        elif level == _Level.CRITICAL['name']:
            return _Level.CRITICAL
        else:
            raise LoggerLevelExcepiton(level)


class _Logger:
    lock_print = False
    lock_save = False

    def __init__(self, name, domain, path, print_level=Level.DEBUG, save_level=Level.NO_LOGGER):
        self.__name = name
        self.__domain = domain
        self.__path = path
        self.__print_level = _Level.find_level(print_level)
        self.__save_level = _Level.find_level(save_level)

    def __str__(self):
        return self.__name

    def __repr__(self):
        return '<Logger object: \'name\'={}, ' \
               '\'domain\'={}, \'print level\'={}, ' \
               '\'save level\'={}, \'path\'={}>'.format(self.__name, self.__domain,
                                                        self.__print_level['name'],
                                                        self.__save_level['name'], self.__path)

    def _get_name(self):
        return self.__name

    def _get_complete_name(self):
        if self.__domain == self.__name:
            return self.__name
        return self.__domain + '/' + self.__name

    @property
    def print_level(self):
        return self.__print_level

    @print_level.setter
    def print_level(self, level):
        new_level = _Level.find_level(level)
        self.__print_level = new_level

    @property
    def save_level(self):
        return self.__save_level

    @save_level.setter
    def save_level(self, level):
        new_level = _Level.find_level(level)
        self.__save_level = new_level

    def setting(self, print_level=None, save_level=None):
        if print_level is not None:
            self.print_level = print_level

        if save_level is not None:
            self.save_level = save_level

    def info(self, text):
        self.__log(_Level.INFO, text)

    def error(self, text):
        self.__log(_Level.ERROR, text)

    def critical(self, text):
        self.__log(_Level.CRITICAL, text)

    def debug(self, text):
        self.__log(_Level.DEBUG, text)

    def warning(self, text):
        self.__log(_Level.WARNING, text)

    def __log(self, level, text):
        s = self.__formatter(level['name'], text)

        if self.__print_level['level'] <= level['level']:
            string = colors.start + level['color'] + s + colors.stop
            _Logger.__print_log(string)

        if self.__save_level['level'] <= level['level']:
            _Logger.__save_log(s, self.__path)

    def __formatter(self, level, text):
        if len(self._get_complete_name()) > 30:
            name_class = self._get_complete_name()[:3] + '...' + self._get_complete_name()[-24:]
        else:
            name_class = self._get_complete_name()
        time = datetime.now().strftime("%y-%b-%d %H:%M:%S.%f")
        return '{} | {:8} | {:30} | {:80}'.format(time, level, name_class, str(text))

    @staticmethod
    def __save_log(text, path):
        text = text + '\n'
        time = datetime.now().strftime('%Y-%m-%d')

        if path is None:
            path = os.getcwd()

        if not os.path.exists(path + '/logs'):
            os.makedirs(path + '/logs')

        path = path + '/logs/{}.log'.format(time)

        with open(path, 'a') as file:
            file.write(text)

    @staticmethod
    def __print_log(text):
        while _Logger.lock_print:
            pass
        _Logger.lock_print = True
        print(text)
        _Logger.lock_print = False


__configured = False
__domain = 'loggerpy'
__path = None
__logger_tree: [_Logger] = []
__print_level = Level.DEBUG
__save_level = Level.NO_LOGGER

# TODO (decidere se aggiungerlo o meno nel metodo configure) modifica del format della stampa
## decidere se ci possono essere due format differenti per print e save
# INFO regolare per i PATH. Non ci devono essere `/` né all'inizio né alla fine


def configure(domain=None, info=False, print_level=None, save_level=None, path=None):
    global __domain, __print_level, __save_level, __logger_tree, __path, __configured

    if not __configured:
        #TODO aggiungere un warning e sistemare il __path
        pass

    if domain is not None:
        __domain = domain

    if path is not None:
        if path[0] == '/':
            path = path[1:]
        if path[-1:] == '/':
            path = path[:-1]
        path = os.getcwd() + '/' + path
    else:
        path = os.getcwd()

    __path = path

    logger = _Logger(__domain, __domain, path)
    __logger_tree.append(logger)

    if print_level is not None:
        logger.print_level = print_level
        __print_level = print_level

    if save_level is not None:
        logger.save_level = save_level
        __save_level = save_level

    if info:
        logger.critical('Logger configured...')


def get_logger(name, print_level=None, save_level=None, path=None):
    global __domain, __logger_tree, __save_level, __print_level, __path

    if name is None:
        raise LoggerNameException('The input name is None')
    elif name == '' or name == '\n' or name == '\t':
        raise LoggerNameException('The input name is empty or a special character')

    if path is not None:
        if path[0] == '/':
            path = path[1:]
        if path[-1:] == '/':
            path = path[:-1]

        if __path is None:
            path = os.getcwd() + '/' + path
        else:
            path = __path + '/' + path
    else:
        if __path is not None:
            #INFO questo controllo dovrebbe essere intuile xk il tutto viene sempre configurato
            path = __path

    if __find_logger(name) is None:
        logger = _Logger(name, __domain, path, print_level=__print_level, save_level=__save_level)
        __logger_tree.append(logger)

    else:
        logger = __find_logger(name)

        if path is not None:
            #TODO aggiungere un warning, tentativo di modifica di un path di un logger già esistente
            pass

    if print_level is not None:
        logger.print_level = print_level

    if save_level is not None:
        logger.save_level = save_level

    return logger


def __find_logger(name):
    for logger in __logger_tree:
        if logger._get_name() is name:
            return logger
    return None
