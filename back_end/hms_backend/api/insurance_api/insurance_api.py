import logging
import traceback
from hms_backend.api.authorization_api import cryptograpy_api
from hms_backend.databases import mongo_db_api
from hms_backend.project_constants import constants, database_constants


def get_insurance_record(user_data):
    """
        This API gets complete insurance details of patient from DB

        Returns: Response with insurance details of patient.
    """
    mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
    try:
        query = {database_constants.USER_USER_ID: user_data[database_constants.USER_USER_ID]}
        required_column = {"_id": 0}
        data = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_INSURANCE, query,
                                      required_column)

        insurance_data = False
        for data_point in data:
            insurance_data = {
                database_constants.INSURANCE_ID: data_point[database_constants.INSURANCE_ID],
                database_constants.INSURANCE_RENEW_DATE: data_point[database_constants.INSURANCE_RENEW_DATE],
                database_constants.INSURANCE_VALIDITY_DATE: data_point[database_constants.INSURANCE_VALIDITY_DATE]
            }
        if insurance_data:
            response = {
                constants.STATUS: constants.STATUS_SUCCESS,
                constants.DATA: insurance_data
            }
        else:
            response = {
                constants.STATUS: constants.STATUS_FAILURE,
                constants.MESSAGE: constants.MESSAGE_INSURANCE_NOT_FOUND
            }
        return response
    except Exception as e:
        logging.error("Application: get_insurance_details() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e
    finally:
        mongo_client.close()


def update_insurance_record(user_data):
    """
        API to add insurance policy to patients

        Args:
            user_data: user information and chosen insurance details

        Return:
            Status: Success or Failure
    """
    try:
        query = {database_constants.USER_USER_ID: user_data[database_constants.USER_USER_ID]}
        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        count = mongo_db_api.count_document_in_search_query(mongo_client, constants.DATABASE_HMS,
                                                            constants.COLLECTION_INSURANCE, query)

        update_data = {"$set": {database_constants.INSURANCE_ID: user_data[database_constants.INSURANCE_ID],
                              database_constants.USER_USER_ID: user_data[database_constants.USER_USER_ID],
                              database_constants.INSURANCE_RENEW_DATE: user_data[database_constants.INSURANCE_RENEW_DATE],
                              database_constants.INSURANCE_VALIDITY_DATE: user_data[database_constants.INSURANCE_VALIDITY_DATE]}}

        insert_data = {
            database_constants.INSURANCE_ID: user_data[database_constants.INSURANCE_ID],
            database_constants.USER_USER_ID: user_data[database_constants.USER_USER_ID],
            database_constants.INSURANCE_RENEW_DATE: user_data[database_constants.INSURANCE_RENEW_DATE],
            database_constants.INSURANCE_VALIDITY_DATE: user_data[database_constants.INSURANCE_VALIDITY_DATE]
        }

        if count != 0:
            mongo_db_api.update_one_into_db(mongo_client, constants.DATABASE_HMS,
                                            constants.COLLECTION_INSURANCE, query,
                                            update_data)
        else:
            mongo_db_api.insert_one_into_db(mongo_client, constants.DATABASE_HMS,
                                        constants.COLLECTION_INSURANCE,
                                        insert_data)
        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.MESSAGE: constants.MESSAGE_INSURANCE_POLICY_ADDED
        }
        return response
    except Exception as e:
        logging.error("Application: create_policy_to_patients() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e
    finally:
        mongo_client.close()


def get_insurance_to_approve():
    mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
    try:
        query = {database_constants.TRANSACTION_USER_TYPE: constants.WAITING_INSURANCE_APPROVAL}
        data_points = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS,
                                             constants.COLLECTION_TRANSACTION, query)

        results = []
        for data in data_points:
            appointment_data = {
                database_constants.TRANSACTION_ID: data[database_constants.TRANSACTION_ID],
                database_constants.APPOINTMENT_USER_ID: data[database_constants.APPOINTMENT_USER_ID],
                database_constants.TRANSACTION_USER_EMAIL:
                    cryptograpy_api.decode(data[database_constants.TRANSACTION_USER_EMAIL]),
                database_constants.TRANSACTION_REASON: cryptograpy_api.decode(data[database_constants.TRANSACTION_DETAILS][database_constants.TRANSACTION_REASON])
            }
            results.append(appointment_data)
        return results
    except Exception as e:
        logging.error(
            "Application: get_transactions_to_initiate() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e
    finally:
        mongo_client.close()


def approve_reject_transactions(post_data):
    mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
    try:
        transaction_id = post_data[database_constants.TRANSACTION_ID]
        query = {"$and": [{database_constants.TRANSACTION_ID: transaction_id},
                          {database_constants.TRANSACTION_USER_TYPE: constants.WAITING_INSURANCE_APPROVAL}]}
        count = mongo_db_api.count_document_in_search_query(mongo_client, constants.DATABASE_HMS,
                                                            constants.COLLECTION_TRANSACTION, query)

        if count == 0:
            raise Exception

        status = constants.INITIATED if post_data[database_constants.TRANSACTION_STATUS] == constants.INITIATED else constants.REJECTED
        new_value = {"$set": {
            database_constants.TRANSACTION_ID: post_data[database_constants.TRANSACTION_ID],
            database_constants.TRANSACTION_USER_TYPE: status,
        }}

        mongo_db_api.update_one_into_db(mongo_client=mongo_client, database_name=constants.DATABASE_HMS,
                                        collection_name=constants.COLLECTION_TRANSACTION, filter_query=query,
                                        new_value=new_value)

        # Code for blockchain here

        response = {
                constants.STATUS: constants.STATUS_SUCCESS,
                constants.MESSAGE: constants.MESSAGE_CHANGE_TRANSACTION_STATUS + status
            }

        return response

    except Exception as e:
        logging.error("Application: get_transactions_to_initiate() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e
    finally:
        mongo_client.close()


def get_insurance_record_from_insurance_id(user_data):
    """
        This API gets complete insurance details of patient from DB

        Returns: Response with insurance details of patient.
    """
    mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
    try:
        query = {database_constants.INSURANCE_ID: user_data[database_constants.INSURANCE_ID]}
        required_column = {"_id": 0}
        data = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_INSURANCE, query,
                                      required_column)

        insurance_data = False
        for data_point in data:
            insurance_data = {
                database_constants.USER_USER_ID: data_point[database_constants.USER_USER_ID],
                database_constants.INSURANCE_ID: data_point[database_constants.INSURANCE_ID],
                database_constants.INSURANCE_RENEW_DATE: data_point[database_constants.INSURANCE_RENEW_DATE],
                database_constants.INSURANCE_VALIDITY_DATE: data_point[database_constants.INSURANCE_VALIDITY_DATE]
            }
        if insurance_data:
            response = {
                constants.STATUS: constants.STATUS_SUCCESS,
                constants.DATA: insurance_data
            }
        else:
            response = {
                constants.STATUS: constants.STATUS_FAILURE,
                constants.MESSAGE: constants.MESSAGE_INSURANCE_NOT_FOUND
            }
        return response
    except Exception as e:
        logging.error("Application: get_insurance_details() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e
    finally:
        mongo_client.close()
