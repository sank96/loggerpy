if __name__ == '__main__':
    from loggerpy import *

    configure()

    logger = get_logger('first', print_level=Level.WARNING, save_level=Level.INFO, path='custom_logger')

    logger.debug('Debug test')
    logger.info('Info test')
    logger.warning('Warning test')
    logger.error('Error test')
    logger.critical('Critical test')