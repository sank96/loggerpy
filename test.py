
if __name__ == '__main__':
    import loggerpy
    from loggerpy import Level

    loggerpy.configure(info=True, save_level=Level.ERROR, path='test/')

    logger = loggerpy.get_logger('test')

    logger.debug('prova')
    logger.info('prova')
    logger.warning('prova')
    logger.error('prova')
    logger.critical('prova')

    logger1 = loggerpy.get_logger('path', save_level=Level.DEBUG, path='pippo/log')

    logger1.debug('prova')
    logger1.info('prova')
    logger1.warning('prova')
    logger1.error('prova')
    logger1.critical('prova')

    print(logger)
    print(repr(logger))
    print(hash(logger))

    logger2 = loggerpy.get_logger('test')

    print(repr(logger2))
    print(hash(logger2))
    print(isinstance(logger, loggerpy._Logger))

    print(logger == logger2)

    print(repr(logger1))

    logger1.setting(print_level=Level.DEBUG, save_level=Level.DEBUG)
    print(logger1.print_level)
    print(logger1.save_level)

    logger1.debug('debug')
    logger1.info('debug')
    logger1.warning('debug')
    logger1.error('debug')
    logger1.critical('debug')

    logger1.setting(print_level=Level.INFO, save_level=Level.INFO)
    print(logger1.print_level)
    print(logger1.save_level)

    logger1.debug('info')
    logger1.info('info')
    logger1.warning('info')
    logger1.error('info')
    logger1.critical('info')

    logger1.setting(print_level=Level.WARNING, save_level=Level.WARNING)
    print(logger1.print_level)
    print(logger1.save_level)

    logger1.debug('warning')
    logger1.info('warning')
    logger1.warning('warning')
    logger1.error('warning')
    logger1.critical('warning')

    logger1.setting(print_level=Level.ERROR, save_level=Level.ERROR)
    print(logger1.print_level)
    print(logger1.save_level)

    logger1.debug('error')
    logger1.info('error')
    logger1.warning('error')
    logger1.error('error')
    logger1.critical('error')

    logger1.setting(print_level=Level.CRITICAL, save_level=Level.CRITICAL)
    print(logger1.print_level)
    print(logger1.save_level)

    logger1.debug('critical')
    logger1.info('critical')
    logger1.warning('critical')
    logger1.error('critical')
    logger1.critical('critical')