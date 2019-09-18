if __name__ == '__main__':
    from loggerpy import *

    configure()

    logger = get_logger('unique_name')
    logger1 = get_logger('unique_name')

    print(logger1 == logger)
    print(hash(logger))
    print(hash(logger1))
