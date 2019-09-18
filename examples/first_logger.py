if __name__ == '__main__':
    from loggerpy import *

    configure()

    logger = get_logger('first')

    logger.debug('Debug test')
    logger.info('Info test')
    logger.warning('Warning test')
    logger.error('Error test')
    logger.critical('Critical test')