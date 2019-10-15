import logging

__logger_factory = None


def set_logger_factory(logger_factory):
    global __logger_factory
    __logger_factory = logger_factory


def __get_default_logger(name):
    return logging.getLogger(name)


def get_logger(name):
    global __logger_factory
    if __logger_factory is None:
        return __get_default_logger(name)
    return __logger_factory(name)
