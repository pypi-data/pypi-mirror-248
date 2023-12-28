import logging


def init_logging():
    logger = logging.getLogger("poco")
    logger.setLevel(logging.DEBUG)
    error_filter = logging.Filter()
    error_filter.filter = lambda record: record.levelno == logging.ERROR

    if not logging.getLogger().hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt='[%(asctime)s][%(levelname)s]<%(name)s> %(message)s',
            datefmt='%H:%M:%S'
        )
        handler.setFormatter(formatter)
        handler.addFilter(error_filter)
        logger.addHandler(handler)
    else:
        for handler in logging.getLogger().handlers:
            handler.addFilter(error_filter)



init_logging()

def get_logger(name):
    logger = logging.getLogger(name)
    return logger
