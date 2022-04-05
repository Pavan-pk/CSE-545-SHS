import logging
import math
import random
import traceback

from hms_backend.api.authorization_api import cryptograpy_api
from hms_backend.databases import mongo_db_api, redis_api
from hms_backend.project_constants import constants, database_constants


def user_registration_api(post_data):
    """
        API to registered new user of the application.

        Args:
            post_data: Credential entered by the user in the UI.

        Return:
            Status: Success or Failure
    """
    try:
        query = {"$and": [{database_constants.USER_HASH_EMAIL: cryptograpy_api.hash_encode(post_data[database_constants.
                                                                                           USER_EMAIL])},
                          {database_constants.USER_USER_TYPE: post_data[database_constants.USER_USER_TYPE]}]}
        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        count = mongo_db_api.count_document_in_search_query(mongo_client, constants.DATABASE_HMS,
                                                            constants.COLLECTION_USERS, query)

        if count != 0:
            response = {
                constants.STATUS: constants.STATUS_FAILURE,
                constants.MESSAGE: constants.MESSAGE_USER_EXIST
            }
            return response

        user_id = mongo_db_api.get_next_sequence(mongo_client, constants.DATABASE_HMS,
                                                 constants.COLLECTION_USERS,
                                                 constants.USER_ID)

        registration_data = {
            database_constants.USER_USER_ID: str(user_id),
            database_constants.USER_FULL_NAME: cryptograpy_api.encode(post_data[database_constants.USER_FULL_NAME]),
            database_constants.USER_BIRTH_DATE: post_data[database_constants.USER_BIRTH_DATE],
            database_constants.USER_EMAIL: cryptograpy_api.encode(post_data[database_constants.USER_EMAIL]),
            database_constants.USER_HASH_EMAIL: cryptograpy_api.hash_encode(post_data[database_constants.USER_EMAIL]),
            database_constants.USER_PASSWORD: cryptograpy_api.encode(post_data[database_constants.USER_PASSWORD]),
            database_constants.USER_USER_TYPE: post_data[database_constants.USER_USER_TYPE],
            database_constants.USER_SPECIALITY: post_data[database_constants.USER_SPECIALITY],
            database_constants.USER_VERIFIED: False,
            database_constants.USER_APPROVED: constants.MESSAGE_NOT_APPLICABLE,
        }

        if post_data[database_constants.USER_USER_TYPE] != "1" and post_data[database_constants.USER_USER_TYPE] != "6":
            registration_data[database_constants.USER_APPROVED] = constants.CREATED

        if post_data[database_constants.USER_USER_TYPE] == "6":
            registration_data[database_constants.USER_VERIFIED] = True

        mongo_db_api.insert_one_into_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_USERS,
                                        registration_data)

        mongo_client.close()
        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.MESSAGE: constants.MESSAGE_USER_ADDED
        }
        return response
    except Exception as e:
        logging.error("Application: user_registration_api() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def user_login_api(post_data):
    """
        API to validate user credential.

         Args:
            post_data: Credential entered by the user in the UI.

        Return:
            Status: Success or Failure
    """
    try:
        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        query = {"$and": [{database_constants.USER_HASH_EMAIL: cryptograpy_api.hash_encode(post_data[database_constants.
                                                                                           USER_EMAIL])},
                          {database_constants.USER_USER_TYPE: post_data[database_constants.USER_USER_TYPE]}]}

        count = mongo_db_api.count_document_in_search_query(mongo_client, constants.DATABASE_HMS,
                                                            constants.COLLECTION_USERS, query)
        if count == 0:
            response = {
                constants.STATUS: constants.STATUS_FAILURE,
                constants.MESSAGE: constants.MESSAGE_USER_NOT_EXIST
            }
            return response

        user_data = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_USERS, query)

        if not user_data[0][database_constants.USER_VERIFIED]:
            response = {
                constants.STATUS: constants.STATUS_FAILURE,
                constants.MESSAGE: constants.MESSAGE_USER_NOT_VERIFIED
            }
            return response

        if user_data[0][database_constants.USER_USER_TYPE] != "1" and \
                user_data[0][database_constants.USER_USER_TYPE] != "6" and \
                user_data[0][database_constants.USER_APPROVED] != constants.STATUS_APPROVED:
            response = {
                constants.STATUS: constants.STATUS_FAILURE,
                constants.MESSAGE: constants.MESSAGE_USER_NOT_APPROVED
            }
            return response

        password = post_data[database_constants.USER_PASSWORD]
        db_password = cryptograpy_api.decode(user_data[0][database_constants.USER_PASSWORD])
        if password == db_password:
            response = {
                constants.STATUS: constants.STATUS_SUCCESS,
                constants.MESSAGE: constants.MESSAGE_USER_LOGIN
            }
            return response

        mongo_client.close()
        response = {
            constants.STATUS: constants.STATUS_FAILURE,
            constants.MESSAGE: constants.MESSAGE_USER_PASSWORD_INCORRECT
        }
        return response
    except Exception as e:
        logging.error("Application: user_login_api() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def generate_otp():
    """
        API to generate OTP if user have added valid credential.

        Return:
            OTP (str)
    """
    digits = "0123456789"
    OTP = ""

    for i in range(6):
        OTP += digits[math.floor(random.random() * len(digits))]

    return OTP


def user_confirm_otp_api(post_data, redis, email_address):
    """
        Verifying user entered otp.

        Args:
            post_data: Credential entered by the user in the UI.
            redis: redis key value in memory db.
            email_address: user email address

        Return:
            Status: Success or Failure
    """
    try:
        user_entered_otp = post_data[constants.OTP_KEY]
        otp_from_redis = redis_api.get_from_redis(redis_client=redis, key=email_address,
                                                  extended_key=constants.REDIS_OTP_EXTENDED_KEY)

        if otp_from_redis is not None and otp_from_redis == user_entered_otp:
            response = {
                constants.STATUS: constants.STATUS_SUCCESS,
                constants.MESSAGE: constants.MESSAGE_OTP_CONFIRMED_SUCCESSFULLY
            }
        elif otp_from_redis is not None and otp_from_redis != user_entered_otp:
            response = {
                constants.STATUS: constants.STATUS_FAILURE,
                constants.MESSAGE: constants.MESSAGE_INCORRECT_OTP
            }
        else:
            response = {
                constants.STATUS: constants.STATUS_FAILURE,
                constants.MESSAGE: constants.MESSAGE_OTP_EXPIRED
            }

        return response
    except Exception as e:
        logging.error("Application: user_confirm_otp_api() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def user_confirm_identity_otp_api(post_data, redis):
    """
        Verifying user entered otp after verifying user who forgot their password.

        Args:
            post_data: Credential entered by the user in the UI.
            redis: redis key value in memory db.

        Return:
            Status: Success or Failure
    """
    try:
        email_address = post_data[database_constants.USER_EMAIL]
        user_entered_otp = post_data[constants.OTP_KEY]
        otp_from_redis = redis_api.get_from_redis(redis_client=redis, key=email_address,
                                                  extended_key=constants.REDIS_OTP_EXTENDED_KEY)

        if otp_from_redis is not None and otp_from_redis == user_entered_otp:
            response = {
                constants.STATUS: constants.STATUS_SUCCESS,
                constants.MESSAGE: constants.MESSAGE_OTP_CONFIRMED_SUCCESSFULLY
            }
        elif otp_from_redis is not None and otp_from_redis != user_entered_otp:
            response = {
                constants.STATUS: constants.STATUS_FAILURE,
                constants.MESSAGE: constants.MESSAGE_INCORRECT_OTP
            }
        else:
            response = {
                constants.STATUS: constants.STATUS_FAILURE,
                constants.MESSAGE: constants.MESSAGE_OTP_EXPIRED
            }

        return response
    except Exception as e:
        logging.error("Application: user_confirm_identity_otp_api() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def user_forgot_password_api(post_data):
    """
        Updating user password with new password after verifying user.

         Args:
            post_data: Credential entered by the user in the UI.

        Return:
            Status: Success or Failure
    """
    try:
        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        query = {"$and": [{database_constants.USER_HASH_EMAIL: cryptograpy_api.hash_encode(post_data[database_constants.
                                                                                           USER_EMAIL])},
                          {database_constants.USER_USER_TYPE: post_data[database_constants.USER_USER_TYPE]}]}

        count = mongo_db_api.count_document_in_search_query(mongo_client, constants.DATABASE_HMS,
                                                            constants.COLLECTION_USERS, query)
        if count == 0:
            response = {
                constants.STATUS: constants.STATUS_FAILURE,
                constants.MESSAGE: constants.MESSAGE_USER_NOT_EXIST
            }
            return response

        password = post_data[database_constants.USER_PASSWORD]
        new_value = {"$set": {database_constants.USER_PASSWORD: cryptograpy_api.encode(password)}}
        mongo_db_api.update_one_into_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_USERS, query,
                                        new_value)
        mongo_client.close()
        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.MESSAGE: constants.MESSAGE_USER_PASSWORD_UPDATE_SUCCESSFULLY
        }
        return response
    except Exception as e:
        logging.error("Application: user_login_api() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def check_user_exists(post_data):
    """
    Check if email id exists

    Args:
        post_data: Json with {email, user_type} keys.

    Returns:
        boolean: Status indicating if user exists or not
    """
    mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
    query = {"$and": [{database_constants.USER_HASH_EMAIL: cryptograpy_api.hash_encode(post_data[database_constants.
                                                                                       USER_EMAIL])},
                      {database_constants.USER_USER_TYPE: post_data[database_constants.USER_USER_TYPE]}]}

    count = mongo_db_api.count_document_in_search_query(mongo_client, constants.DATABASE_HMS,
                                                        constants.COLLECTION_USERS, query)

    if count: return True
    return False
