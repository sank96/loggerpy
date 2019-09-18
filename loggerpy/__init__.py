import os
from datetime import datetime

from loggerpy.logger_exception import LoggerNameException, LoggerLevelException, LoggerPathException
from loggerpy.colors import colors

__all__ = ['Level', 'configure', 'get_logger']


class Level(object):
    """
    Useful class that collects all the possible levels
    NO_LOGGER: str
        Neither printing nor saving
    DEBUG: str
    INFO: str
    WARNING: str
    ERROR: str
    CRITICAL: str
    """
    NO_LOGGER = 'NO LOGGER'
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'

    def upper(self):
        return self.upper()


class _Level(object):
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
    find_level(level)
        Return the dict associated to the level in input
    """

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
        """
        It is used to find the dict that represents the level in input
        :param level: desired level
        :type level: Level
        :raise: LoggerLevelException if the input level is not in Level class
        :return: dictionary with all information, including colors, number level and name
        :rtype: dict
        """
        if level is None:
            raise LoggerLevelException('NONE')

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
            raise LoggerLevelException(level)


class _Logger(object):
    """
    Logger class provides all the tools needed to log everything
    ...
    Attributes
    ----------
    __name: str
        The name of the logger useful to find an instance of the logger from get_logger()
    __domain: str
        The entire domain of the logger, if it is generated in su subpackage of the project
    __path: str
        The path to save the log. Default value it the path of the project
    __print_level: Level
        The level of print logging
    __save_level: Level
        The level of save logging

    Methods
    -------
    setting(print_level, save_level)
        Customize the property of printing and saving level of the logger
    debug(test)
        Print debug log
    info(text)
        Print info log
    warning(text)
        Print warning log
    error(text)
        Print error log
    critical(text)
        Print critical log

    Properties
    ----------
    print_level: Level
        Allows to modified the __print_level attribute
    save_level: Level
        Allows to modified the __save_level attribute
    """
    lock_print = False
    lock_save = False

    def __init__(self, name, domain, path,
                 print_level: Level = Level.DEBUG,
                 save_level: Level = Level.NO_LOGGER):
        """
        Create an instance of the logger
        :param name: Name of logger
        :type name: str
        :param domain: domain of logger if you want a sub domain
        :type domain: str
        :param path: path of saving
        :type path: str
        :param print_level: level of printing log
        :type print_level: Level
        :param save_level: level of saving log
        :type save_level: Level
        """
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
        """
        Return the name of the logger
        :return: name of logger
        :rtype: str
        """
        return self.__name

    def _get_complete_name(self):
        """
        Return the complete name of logger
        :return: domain + name of the logger as a path
        :rtype: str
        """
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
        """
        Change the setting of printing and saving logging
        :param print_level: custom level of printing log
        :type print_level: Level
        :param save_level: custom level of saving log
        :type save_level: Level
        :return: No object be returned
        :rtype: None
        """
        if print_level is not None:
            self.print_level = print_level

        if save_level is not None:
            self.save_level = save_level

    def info(self, text):
        """
        Print an _info_ log
        :param text: body of log
        :type text: str
        """
        self.__log(_Level.INFO, text)

    def error(self, text):
        """
        Print an _error_ log
        :param text: body of log
        :type text: str
        """
        self.__log(_Level.ERROR, text)

    def critical(self, text):
        """
        Print an _critical_ log
        :param text: body of log
        :type text: str
        """
        self.__log(_Level.CRITICAL, text)

    def debug(self, text):
        """
        Print an _debug_ log
        :param text: body of log
        :type text: str
        """
        self.__log(_Level.DEBUG, text)

    def warning(self, text):
        """
        Print an _warning_ log
        :param text: body of log
        :type text: str
        """
        self.__log(_Level.WARNING, text)

    def __log(self, level: _Level, text: str):
        """
        This hidden method prepares the setting to print and save the log, depending on the chosen level
        :param level: level of printing and saving log
        :type level: _Level
        :param text: body of printing or saving log
        :type text: str
        """
        s = self.__formatter(level['name'], text)

        if self.__print_level['level'] <= level['level']:
            string = colors.start + level['color'] + s + colors.stop
            _Logger.__print_log(string)

        if self.__save_level['level'] <= level['level']:
            _Logger.__save_log(s, self.__path)

    def __formatter(self, level, text):
        """
        Depends on the level, formats the logging string
        :param level: level of loggin
        :type level: str
        :param text: body of logging
        :type text: str
        :return: completed string, composed by: timestamp + domain of logger + name of logger + logging message
        :rtype: str
        """
        if len(self._get_complete_name()) > 30:
            name_class = self._get_complete_name()[:3] + '...' + self._get_complete_name()[-24:]
        else:
            name_class = self._get_complete_name()
        time = datetime.now().strftime("%y-%b-%d %H:%M:%S.%f")
        return '{} | {:8} | {:30} | {:80}'.format(time, level, name_class, str(text))

    @staticmethod
    def __save_log(text, path):
        """
        This method saves the log given as input in the specified path
        :param text: log message
        :type text: str
        :param path: path of the folder in which save logs
        :type path: str
        """
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
        """
        This method print the log on the stdout. It is developed for multi threads logging
        :param text: log message
        :type text: str
        """
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


def configure(domain=None, info=False, print_level=None, save_level=None, path=None):
    """
    This method manages all the possible configuration of loggerpy package.
    If it is not configured a warning stamp is printed and it is configured with default setting
    :param domain: Main domain of logger. This can not be change after the first initialization
    :type domain: str
    :param info: If you want to print an info message at the first configuration
    :type info: bool
    :param print_level: set the default print level
    :type print_level: Level
    :param save_level: set the default save level
    :type save_level: Level
    :param path: Set the path to save log. It is not relevant if path contains '/' at the beginning or at the
        end, it is always managed
    :type path: str
    """
    global __domain, __print_level, __save_level, __logger_tree, __path, __configured

    # fixme: manage the insert of space into path. I can create a function that validate the path
    #  (space, '/', special character)
    if path == '' or path == '\n' or path == '\t':
        raise LoggerPathException(path)

    if __configured:
        if print_level is not None:
            __print_level = print_level

        if save_level is not None:
            __save_level = save_level

    else:
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
            # next: make the text customizable
            # next: make the log level customizable

        __configured = True


def get_logger(name, print_level=None, save_level=None, path=None):
    """
    This method allows to instance a logger object.
    If it is given a name that correspond to another already logger instanced, it is returned. In this case the path
    can not be changed.
    :param name: Name of the logger
    :type name: str
    :param print_level: level of print logging
    :type print_level: Level
    :param save_level:  level of save logging
    :type save_level: Level
    :param path: path of save logging
    :type path: str
    :return: return the logger with the input configuration
    :rtype: _Logger
    """
    global __domain, __logger_tree, __save_level, __print_level, __path, __configured

    if not __configured:
        import warnings
        warnings.warn('No configurations are done. The default setting are used.')
        path = os.getcwd()
        configure(path=path)
        __configured = True

    if name is None:
        raise LoggerNameException('The input name is None')
    elif name == '' or name == '\n' or name == '\t':
        raise LoggerNameException('The input name is empty or a special character')

    if path == '' or path == '\n' or path == '\t':
        raise LoggerPathException(path)

    if path is not None:
        complete_path = path
        if complete_path[0] == '/':
            complete_path = complete_path[1:]
        if complete_path[-1:] == '/':
            complete_path = complete_path[:-1]

        if __path is None:
            complete_path = os.getcwd() + '/' + complete_path
        else:
            complete_path = __path + '/' + complete_path
    else:
        complete_path = __path

    if __find_logger(name) is None:
        logger = _Logger(name, __domain, complete_path, print_level=__print_level, save_level=__save_level)
        __logger_tree.append(logger)

    else:
        logger = __find_logger(name)

        if path is not None:
            import warnings
            warnings.warn('The input name corresponds to an already existing logger and it is trying to '
                          'modify the saving path. This modification is not allowed so it is not applied.',
                          stacklevel=2)
            pass

    if print_level is not None:
        logger.print_level = print_level

    if save_level is not None:
        logger.save_level = save_level

    return logger


def __find_logger(name):
    """
    This method search a logger in logger_tree with the name as input
    :param name: input name
    :type name: str
    :return: Return an instance of the logger if found, otherwise return None
    :rtype: _Logger
    """
    for logger in __logger_tree:
        if logger._get_name() is name:
            return logger
    return None
