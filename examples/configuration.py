if __name__ == '__main__':
    from loggerpy import Logger, Level

    logger = Logger()
    logger.configure(name="configuration", print_level=Level.DEBUG)

    STR = 'CONFIGURATION very long'

    logger.debug('Debug test', source=STR)
    logger.info('Info test', source=STR)
    logger.warning('Warning test', source=STR)
    logger.error('Error test', source=STR)
    logger.critical('Critical test', source=STR)
