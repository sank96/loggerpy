if __name__ == '__main__':
    from loggerpy import Logger, Level

    logger = Logger()
    logger.configure(name="Configuration", print_level=Level.ERROR)

    logger.debug('Debug test')
    logger.info('Info test')
    logger.warning('Warning test')
    logger.error('Error test')
    logger.critical('Critical test')
