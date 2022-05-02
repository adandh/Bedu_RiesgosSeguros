import logging
formatter = logging.Formatter(fmt='%(levelname)s:%(message)s')
# '%(asctime)s %(levelname)s %(message)s'

def set_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger