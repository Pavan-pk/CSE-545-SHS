import logging
import traceback
import requests
from _datetime import datetime, timedelta
from hms_backend.api.authorization_api import cryptograpy_api
from hms_backend.databases import mongo_db_api
from hms_backend.project_constants import constants, database_constants
from flask import current_app as app
import base64


def get_new_created_account():
    try:
        query = {"$and": [{database_constants.USER_VERIFIED: True},
                          {database_constants.USER_APPROVED: constants.CREATED}]}

        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        count = mongo_db_api.count_document_in_search_query(mongo_client, constants.DATABASE_HMS,
                                                            constants.COLLECTION_USERS, query)

        if count == 0:
            response = {
                constants.STATUS: constants.STATUS_SUCCESS,
                constants.MESSAGE: constants.MESSAGE_NO_APPROVAL_PENDING
            }
            return response

        new_users_data = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_USERS, query)

        results = []
        for data in new_users_data:
            new_user_object = {
                database_constants.USER_USER_ID: data[database_constants.USER_USER_ID],
                database_constants.USER_FULL_NAME: cryptograpy_api.decode(data[database_constants.USER_FULL_NAME]),
                database_constants.USER_BIRTH_DATE: data[database_constants.USER_BIRTH_DATE],
                database_constants.USER_EMAIL: cryptograpy_api.decode(data[database_constants.USER_EMAIL]),
                database_constants.USER_USER_TYPE: data[database_constants.USER_USER_TYPE],
                database_constants.USER_SPECIALITY: data[database_constants.USER_SPECIALITY],
                database_constants.USER_VERIFIED: data[database_constants.USER_VERIFIED],
                database_constants.USER_APPROVED: data[database_constants.USER_APPROVED]
            }

            results.append(new_user_object)

        mongo_client.close()
        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.DATA: results
        }
        return response
    except Exception as e:
        logging.error("Application: get_new_created_account() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def approve_new_account(post_data):
    try:
        query = {database_constants.USER_USER_ID: post_data[database_constants.USER_USER_ID]}

        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)

        new_value = {"$set": {database_constants.USER_APPROVED: post_data[database_constants.USER_APPROVED]}}

        mongo_db_api.update_one_into_db(mongo_client=mongo_client, database_name=constants.DATABASE_HMS,
                                        collection_name=constants.COLLECTION_USERS, filter_query=query,
                                        new_value=new_value)

        mongo_client.close()

        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.MESSAGE: constants.MESSAGE_USER_APPROVED_OR_REJECT
        }
        return response
    except Exception as e:
        logging.error("Application: approve_new_account() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def add_log_message(message):
    try:
        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        current_time = datetime.today()
        date_time_string = current_time.strftime("%m/%d/%Y, %H:%M:%S")
        current_time = current_time.isoformat()

        log_id = mongo_db_api.get_next_sequence(mongo_client, constants.DATABASE_HMS,
                                                constants.COLLECTION_ADMIN_LOG, database_constants.ADMIN_LOG_ID)

        log_record = {
            database_constants.ADMIN_LOG_ID: log_id,
            database_constants.ADMIN_LOG_DATE: current_time,
            database_constants.ADMIN_LOG_TIME: date_time_string,
            database_constants.ADMIN_LOG_MESSAGE: cryptograpy_api.encode(message)
        }

        mongo_db_api.insert_one_into_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_ADMIN_LOG,
                                        log_record)

        mongo_client.close()
    except Exception as e:
        logging.error("Application: add_log_message() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def get_admin_logs():
    try:
        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        current_date = datetime.today()
        day = int(current_date.strftime("%d"))
        month = int(current_date.strftime("%m"))
        year = int(current_date.strftime("%Y"))
        hour = int(current_date.strftime("%H"))
        minute = int(current_date.strftime("%M"))
        current_date = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=0).isoformat()

        past_date = datetime.today() - timedelta(days=1)
        day = int(past_date.strftime("%d"))
        month = int(past_date.strftime("%m"))
        year = int(past_date.strftime("%Y"))
        hour = int(past_date.strftime("%H"))
        minute = int(past_date.strftime("%M"))
        past_date = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=0).isoformat()

        query = {"$and": [{database_constants.ADMIN_LOG_DATE: {"$gte": past_date}},
                          {database_constants.ADMIN_LOG_DATE: {"$lt": current_date}}]}

        log_data_points = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS,
                                                 constants.COLLECTION_ADMIN_LOG, query)

        results = []
        msg = ""
        for data in log_data_points:
            log_data = {
                database_constants.ADMIN_LOG_ID: data[database_constants.ADMIN_LOG_ID],
                database_constants.ADMIN_LOG_TIME: data[database_constants.ADMIN_LOG_TIME],
                database_constants.ADMIN_LOG_MESSAGE: cryptograpy_api.decode(
                    data[database_constants.ADMIN_LOG_MESSAGE])
            }

            results.append(log_data)

        if len(results) == 0:
            msg = constants.MESSAGE_NO_ACTIVITIES_FROM_ANY_USER

        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.DATA: results,
            constants.MESSAGE: msg
        }

        return response
    except Exception as e:
        logging.error("Application: get_admin_logs() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def delete_user_record(post_data):
    mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
    try:
        query = {database_constants.USER_USER_ID: post_data[database_constants.USER_USER_ID]}
        user_data_points = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS,
                                                 constants.COLLECTION_USERS, query)
        user_type = "0"
        for points in user_data_points:
            user_type = points[database_constants.USER_USER_TYPE]
        if user_type == "6":
            return {
                constants.STATUS: constants.STATUS_FAILURE,
                constants.MESSAGE: constants.MESSAGE_ADMIN_ACCOUNT_DELETE
            }
        mongo_db_api.delete_one_document(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_USERS, query)
        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.MESSAGE: constants.MESSAGE_USER_RECORD_DELETED_SUCCESSFULLY
        }
        return response
    except Exception as e:
        logging.error("Application: delete_user_record() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e
    finally:
        mongo_client.close()


def get_transactions_to_approve():
    mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
    try:
        query = {"$and": [{database_constants.TRANSACTION_USER_TYPE: constants.INITIATED}]}
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
            "Application: get_transactions_to_approve() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e
    finally:
        mongo_client.close()


def approve_reject_transactions(post_data):
    mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
    try:
        transaction_id = post_data[database_constants.TRANSACTION_ID]
        query = {"$and": [{database_constants.TRANSACTION_ID: transaction_id},
                          {database_constants.TRANSACTION_USER_TYPE: constants.INITIATED}]}
        count = mongo_db_api.count_document_in_search_query(mongo_client, constants.DATABASE_HMS,
                                                            constants.COLLECTION_TRANSACTION, query)
        if count == 0:
            raise Exception

        status = constants.APPROVED if post_data[database_constants.TRANSACTION_STATUS] == constants.APPROVED else constants.REJECTED
        new_value = {"$set": {
            database_constants.TRANSACTION_ID: post_data[database_constants.TRANSACTION_ID],
            database_constants.TRANSACTION_USER_TYPE: status,
        }}

        mongo_db_api.update_one_into_db(mongo_client=mongo_client, database_name=constants.DATABASE_HMS,
                                        collection_name=constants.COLLECTION_TRANSACTION, filter_query=query,
                                        new_value=new_value)

        if status == constants.APPROVED:
            query = {"$and": [{database_constants.TRANSACTION_ID: transaction_id},
                              {database_constants.TRANSACTION_USER_TYPE: constants.APPROVED}]}

            required_column = {"_id": 0}
            transaction_data = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS,
                                                      constants.COLLECTION_TRANSACTION, query, required_column)

            record = None
            for data in transaction_data:
                record = data
                record[database_constants.TRANSACTION_USER_EMAIL] = base64.b64encode(
                    record[database_constants.TRANSACTION_USER_EMAIL]).decode('ascii')
                record_transaction_details = record[database_constants.TRANSACTION_DETAILS]

                record_transaction_details[database_constants.TRANSACTION_AMOUNT] = base64.b64encode(
                    record_transaction_details[database_constants.TRANSACTION_AMOUNT]).decode('ascii')
                record_transaction_details[database_constants.TRANSACTION_REASON] = base64.b64encode(
                    record_transaction_details[database_constants.TRANSACTION_REASON]).decode('ascii')
                record[database_constants.TRANSACTION_DETAILS] = "AMOUNT: "+\
                                                                 record_transaction_details[
                                                                     database_constants.TRANSACTION_AMOUNT] + "|||" +\
                                                                 "REASON: "+\
                                                                 record_transaction_details[
                                                                     database_constants.TRANSACTION_REASON]

        response = {
                constants.STATUS: constants.STATUS_SUCCESS,
                constants.MESSAGE: constants.MESSAGE_CHANGE_TRANSACTION_STATUS + status,
                constants.DATA: record
        }

        return response

    except Exception as e:
        logging.error("Application: approve_reject_transactions() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e
    finally:
        mongo_client.close()
