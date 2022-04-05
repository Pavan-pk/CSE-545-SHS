import json
import hms_backend.project_constants.constants as constants
import logging
import traceback
from flask import current_app as app


def get_application_configuration():
    """
        This function is used to get the application configuration from file as per the working environment.
        Environment: development and production.

        Return:
             Json app config object
    """
    try:
        if app.config[constants.ENVIRONMENT] == constants.ENV_PROD:
            with open('/etc/ss_backend_config/ss_backend_config.json') as config_file:
                backend_config = json.load(config_file)
        else:
            with open('../../app_configuration/ss_backend_config_dev.json') as config_file:
                backend_config = json.load(config_file)
        return backend_config
    except Exception as e:
        logging.error("Configuration error: " + str(e) + "\n" + traceback.format_exc())
        return None
