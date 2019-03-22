import logging

db_logger = None


def init_logger():
    global db_logger
    # create logger
    logger_name = "db_check_logger"
    db_logger = logging.getLogger(logger_name)

    db_logger.setLevel(logging.DEBUG)

    # create file handler
    log_path = "./db_check.log"
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.WARNING)

    # create stream handler
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)

    # create formatter
    fmt = "%(asctime)s [%(levelname)s][%(filename)s:%(lineno)d][%(funcName)s] : %(message)s"
    datefmt = "%m/%d/%Y %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)

    # add handler and formatter to logger
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    db_logger.addHandler(fh)
    db_logger.addHandler(sh)


def logger():
    return db_logger
