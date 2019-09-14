import traceback

if __name__ == '__main__':
    import loggerpy

    loggerpy.configure(info=True, save_level='ERROR', path='test/')

    logger = loggerpy.get_logger('test')

    # logger.info('prova')
    # logger.debug('prova')
    # logger.warning('prova')
    # logger.error('prova')
    # logger.critical('prova')

    logger1 = loggerpy.get_logger('path', save_level='DEBUG', path='pippo/log')

    logger1.info('test path')