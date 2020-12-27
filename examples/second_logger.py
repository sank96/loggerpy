if __name__ == '__main__':
    from loggerpy import Logger, Level

    logger = Logger()
    logger.configure(name="Second logger", log_folder="../test/test", print_level=Level.ERROR, save_level=Level.WARNING)

    logger.debug('Debug test')
    logger.info('Info test')
    logger.warning('Warning test')
    logger.error('Error test')
    logger.critical('Critical test')
