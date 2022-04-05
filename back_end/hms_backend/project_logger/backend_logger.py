import logging
import logging.config
from hms_backend.project_constants import constants
from os import path


def get_logger(name):
    """
        Setting up log for the application

        Args:
            name (str): Filename for which log is set up

        Return:
             logger object
    """
    logging.config.fileConfig(path.join(path.dirname(path.abspath(__file__)), constants.LOG_FILE_NAME))
    log = logging.getLogger(name)
    return log
