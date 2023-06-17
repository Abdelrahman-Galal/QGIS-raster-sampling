import logging
import os

def create_logger(logger_name, log_file, 
                 level=logging.INFO,
                 formatter='%(asctime)s - %(levelname)s - %(message)s',
                 filemode='w',
                 datefmt='%d-%m-%Y %I:%M:%S'):
    """To create loggers"""
    try:
        handler = logging.FileHandler(log_file,mode=filemode)
    except FileNotFoundError:
        dir = os.path.dirname(log_file)
        os.mkdir(dir)
        handler = logging.FileHandler(log_file,mode=filemode)
    
    formatter =  logging.Formatter(formatter,datefmt=datefmt)      
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    for h in logger.handlers:
        h.close()
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.propagate = False
    return logger