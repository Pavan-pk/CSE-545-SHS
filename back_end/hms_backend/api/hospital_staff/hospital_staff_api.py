import logging
import traceback
from datetime import datetime, timedelta
from hms_backend.api.authorization_api import cryptograpy_api
from hms_backend.databases import mongo_db_api
from hms_backend.project_constants import constants, database_constants


def get_requested_appointments():
    """
        This API gets requested appointments

        Returns: Response with requested appointments.
    """
    mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
    try:
        query = {"$and": [{database_constants.APPOINTMENT_STATUS: constants.REQUEST_APPOINTMENT}]}
        appointment_data_points = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS,
                                                         constants.COLLECTION_APPOINTMENTS, query)

        results = []
        msg = ""
        for data in appointment_data_points:
            appointment_data = {
                database_constants.APPOINTMENT_APPOINTMENT_ID: data[database_constants.APPOINTMENT_APPOINTMENT_ID],
                database_constants.APPOINTMENT_TIME: data[database_constants.APPOINTMENT_TIME],
                database_constants.APPOINTMENT_DOCTOR_NAME: cryptograpy_api.decode(
                    data[database_constants.APPOINTMENT_DOCTOR_NAME]),
                database_constants.APPOINTMENT_USER_EMAIL:
                    cryptograpy_api.decode(data[database_constants.APPOINTMENT_USER_EMAIL]),
                database_constants.APPOINTMENT_USER_ID: data[database_constants.APPOINTMENT_USER_ID]
            }
            results.append(appointment_data)

        if len(results) == 0:
            msg = constants.MESSAGE_NO_APPOINTMENT_AVAILABLE

        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.DATA: results,
            constants.MESSAGE: msg
        }

        return response
    except Exception as e:
        logging.error("Application: update_patient_info() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e
    finally:
        mongo_client.close()


def approve_reject_appointment(post_data, approve=True):
    """
        This API approves appointment
        Returns: Response with status.
    """
    mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
    try:
        appointment_id = post_data[database_constants.APPOINTMENT_APPOINTMENT_ID]
        query = {"$and": [{database_constants.APPOINTMENT_APPOINTMENT_ID: appointment_id},
                          {database_constants.APPOINTMENT_STATUS: constants.REQUEST_APPOINTMENT}]}

        count = mongo_db_api.count_document_in_search_query(mongo_client, constants.DATABASE_HMS,
                                                            constants.COLLECTION_APPOINTMENTS, query)

        if count == 0:
            response = {
                constants.STATUS: constants.STATUS_FAILURE,
                constants.MESSAGE: constants.MESSAGE_SLOT_NOT_AVAILABLE
            }
            return response

        reject_approve = constants.BOOKED if approve else constants.AVAILABLE
        new_value = {"$set": {
            database_constants.APPOINTMENT_USER_ID: post_data[database_constants.APPOINTMENT_USER_ID],
            database_constants.APPOINTMENT_USER_EMAIL: cryptograpy_api.encode
            (post_data[database_constants.APPOINTMENT_USER_EMAIL]),
            database_constants.APPOINTMENT_STATUS: reject_approve,
        }}

        mongo_db_api.update_one_into_db(mongo_client=mongo_client, database_name=constants.DATABASE_HMS,
                                        collection_name=constants.COLLECTION_APPOINTMENTS, filter_query=query,
                                        new_value=new_value)

        if approve:
            transaction_id = mongo_db_api.get_next_sequence(mongo_client, constants.DATABASE_HMS,
                                                            constants.COLLECTION_TRANSACTION,
                                                            database_constants.TRANSACTION_ID)

            # Using transaction type to get transaction status.
            transaction_object = {
                database_constants.TRANSACTION_ID: str(transaction_id),
                database_constants.TRANSACTION_USER_ID: post_data[database_constants.USER_USER_ID],
                database_constants.TRANSACTION_USER_TYPE: constants.CREATED,
                database_constants.TRANSACTION_USER_EMAIL: cryptograpy_api.encode(
                    post_data[database_constants.APPOINTMENT_USER_EMAIL]),
                database_constants.TRANSACTION_USER_BIRTH_DATE: "",
                database_constants.TRANSACTION_TYPE: "",
                database_constants.TRANSACTION_DETAILS: {
                    database_constants.TRANSACTION_APPOINTMENT_ID: appointment_id,
                    database_constants.TRANSACTION_REASON: "",
                    database_constants.TRANSACTION_AMOUNT: "",
                }
            }

            mongo_db_api.insert_one_into_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_TRANSACTION,
                                            transaction_object)

        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.MESSAGE: constants.MESSAGE_APPOINTMENT_BOOKED_SUCCESSFULLY
        }
        mongo_client.close()
        return response
    except Exception as e:
        mongo_client.close()
        raise e


def get_transactions_to_initiate():
    mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
    try:
        query = {"$and": [{database_constants.TRANSACTION_USER_TYPE: constants.CREATED}]}
        data_points = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS,
                                                         constants.COLLECTION_TRANSACTION, query)

        results = []
        for data in data_points:
            appointment_data = {
                database_constants.TRANSACTION_ID: data[database_constants.TRANSACTION_ID],
                database_constants.TRANSACTION_USER_EMAIL:
                    cryptograpy_api.decode(data[database_constants.TRANSACTION_USER_EMAIL]),
                database_constants.APPOINTMENT_USER_ID: data[database_constants.APPOINTMENT_USER_ID],
                database_constants.TRANSACTION_APPOINTMENT_ID:
                    data[database_constants.TRANSACTION_DETAILS][database_constants.TRANSACTION_APPOINTMENT_ID]
            }
            results.append(appointment_data)
        return results
    except Exception as e:
        logging.error("Application: get_transactions_to_initiate() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e
    finally:
        mongo_client.close()


def initiate_transaction(post_data):
    mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
    try:
        transaction_id = post_data[database_constants.TRANSACTION_ID]
        query = {"$and": [{database_constants.TRANSACTION_ID: transaction_id},
                          {database_constants.TRANSACTION_USER_TYPE: constants.CREATED}]}
        count = mongo_db_api.count_document_in_search_query(mongo_client, constants.DATABASE_HMS,
                                                            constants.COLLECTION_TRANSACTION, query)
        if count == 0:
            raise Exception

        status = constants.INITIATED if post_data[database_constants.TRANSACTION_TYPE] != constants.INSURANCE else constants.WAITING_INSURANCE_APPROVAL
        new_value = {"$set": {
            database_constants.TRANSACTION_ID: post_data[database_constants.TRANSACTION_ID],
            database_constants.TRANSACTION_USER_TYPE: status,
            database_constants.TRANSACTION_TYPE: post_data[database_constants.TRANSACTION_TYPE],
            database_constants.TRANSACTION_DETAILS: {
                database_constants.TRANSACTION_APPOINTMENT_ID: post_data[database_constants.TRANSACTION_APPOINTMENT_ID],
                database_constants.TRANSACTION_REASON: cryptograpy_api.encode(post_data[database_constants.TRANSACTION_REASON]),
                database_constants.TRANSACTION_AMOUNT: cryptograpy_api.encode(post_data[database_constants.TRANSACTION_AMOUNT])
            }
        }}

        mongo_db_api.update_one_into_db(mongo_client=mongo_client, database_name=constants.DATABASE_HMS,
                                        collection_name=constants.COLLECTION_TRANSACTION, filter_query=query,
                                        new_value=new_value)
        return
    except Exception as e:
        logging.error("Application: get_transactions_to_initiate() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e
    finally:
        mongo_client.close()

