import os
from datetime import datetime

from loggerpy.logger_exception import LoggerNameException, LoggerLevelExcepiton
from loggerpy.colors import colors


class _Level:
    __list = '[\'NO LOGGER\', \'DEBUG\', \'INFO\', \'WARNING\', \'ERROR\', \'CRITICAL\''

    NO_LEVEL = {'color': colors.get_color(), 'name': 'NO LOGGER', 'level': 5}
    DEBUG = {'color': colors.get_color(fg=colors.fg.blue), 'name': 'DEBUG',
             'level': 0}
    INFO = {'color': colors.get_color(fg=colors.fg.lightgreen), 'name': 'INFO',
            'level': 1}
    WARNING = {'color': colors.get_color(fg=colors.fg.yellow, type=colors.bold), 'name': 'WARNING',
               'level': 2}
    ERROR = {'color': colors.get_color(fg=colors.fg.red), 'name': 'ERROR',
             'level': 3}
    CRITICAL = {'color': colors.get_color(bg=colors.bg.red), 'name': 'CRITICAL',
                'level': 4}

    @staticmethod
    def find_level(level):
        if level is None:
            raise LoggerLevelExcepiton('NONE', _Level.__list)

        level = level.upper()

        if level == _Level.NO_LEVEL['name']:
            return _Level.NO_LEVEL
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
            raise LoggerLevelExcepiton(level, _Level.__list)


class _Logger:
    lock_print = False
    lock_save = False

    def __init__(self, name, domain, print_level=_Level.DEBUG['name'], save_level=_Level.NO_LEVEL['name']):
        self.name = name
        self.domain = domain
        self.path = None
        self.print_level = _Level.find_level(print_level)
        self.save_level = _Level.find_level(save_level)

    def __str__(self):
        return self.name

    def _get_name(self):
        return self.name

    def _get_complete_name(self):
        if self.domain == self.name:
            return self.name
        return self.domain + '/' + self.name

    def set_print_level(self, level='DEBUG'):
        new_level = _Level.find_level(level)
        self.print_level = new_level

    def _get_print_level(self):
        print('print: ' + str(self.print_level))

    def set_save_level(self, level='NO LOGGER'):
        new_level = _Level.find_level(level)
        self.save_level = new_level

    def _get_save_level(self):
        print('save: ' + str(self.save_level))

    def set_path(self, path):
        print(path)
        if os.path.exists(path):
            self.path = path
        else:
            if path[0] == '/':
                path = os.getcwd() + path
            else:
                path = os.getcwd() + '/' + path
                os.makedirs(path)
                self.path = path

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

        if self.print_level['level'] <= level['level']:
            string = colors.start + level['color'] + s + colors.stop
            _Logger.__print_log(string)

        if self.save_level['level'] <= level['level']:
            _Logger.__save_log(s, self.path)

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


__domain = 'loggerpy'
__path = None
__logger_tree: [_Logger] = []
__print_level = _Level.DEBUG['name']
__save_level = _Level.NO_LEVEL['name']

#INFO regolare per i PATH. Non ci devono essere `/` né all'inizio né alla fine


def configure(domain=None, info=False, print_level=None, save_level=None, path=None):
    global __domain, __print_level, __save_level, __logger_tree, __path
    if domain is not None:
        __domain = domain

    logger = _Logger(__domain, __domain)
    __logger_tree.append(logger)

    if print_level is not None:
        logger.set_print_level(print_level)
        __print_level = print_level

    if save_level is not None:
        logger.set_save_level(save_level)
        __save_level = save_level

    if path is not None:

        if path[0] == '/':
            path = path[1:]
        if path[-1:] == '/':
            path = path[:-1]

        __path = path
        logger.set_path(path)

    if info:
        logger.critical('Logger configured...')


def get_logger(name, print_level=None, save_level=None, path=None):
    global __domain, __logger_tree, __save_level, __print_level, __path

    if name is None:
        raise LoggerNameException('The input name is None')
    elif name == '' or name == '\n' or name == '\t':
        raise LoggerNameException('The input name is empty or a special character')

    if __find_logger(name) is None:
        logger = _Logger(name, __domain, print_level=__print_level, save_level=__save_level)
        __logger_tree.append(logger)

    else:
        logger = __find_logger(name)

    if print_level is not None:
        logger.set_print_level(print_level)

    if save_level is not None:
        logger.set_save_level(save_level)

    if path is not None:

        if path[0] == '/':
            path = path[1:]
        if path[-1:] == '/':
            path = path[:-1]

        if __path is None:
            logger.set_path(path)

        else:
            logger.set_path(__path + '/' + path)



    return logger


def __find_logger(name):
    for logger in __logger_tree:
        if logger._get_name() is name:
            return logger
    return None
