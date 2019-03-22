"""
Initialize and provide logger for db_check.
"""
import logging
import os

db_logger = None
log_path = None
log_name = None


def init_logger():
    """
    Create and configure the logger.
    """
    global db_logger
    global log_path
    global log_name
    # create logger
    logger_name = "db_check_logger"
    db_logger = logging.getLogger(logger_name)
    db_logger.setLevel(logging.DEBUG)

    # create file handler
    log_path = "./logs/"
    log_name = "db_check.log"

    os.makedirs(log_path, exist_ok=True)

    fh = logging.FileHandler(log_path+log_name)
    fh.setLevel(logging.DEBUG)

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
    """
    Getter for logger instance.
    """
    return db_logger


def log_path():
    """
    Getter for log path.
    """
    return log_path


def log_name():
    """
    Getter for log path.
    """
    return log_name
