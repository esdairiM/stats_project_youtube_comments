import logging
import logging.config
import os


def init_logger():
    try:
        os.mkdir("../log")
    except FileExistsError:
        pass
    # load the logging configuration
    logging.config.fileConfig(
        '../configuration/logging_config.ini',
        defaults={'logfilename': '../log/logFile.log'}
    )
