if __name__ == '__main__':
    from loggerpy import configure, Level, get_logger

    configure(domain='custom domain',
              path='log',
              print_level=Level.DEBUG,
              save_level=Level.NO_LOGGER,
              info=True
              )

    logger = get_logger('configuration')

    logger.debug('Debug test')
    logger.info('Info test')
    logger.warning('Warning test')
    logger.error('Error test')
    logger.critical('Critical test')

