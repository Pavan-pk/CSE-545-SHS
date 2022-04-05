import logging
import traceback
from datetime import datetime, timedelta
from hms_backend.api.authorization_api import cryptograpy_api
from hms_backend.databases import mongo_db_api
from hms_backend.project_constants import constants, database_constants
from collections import defaultdict


def get_requested_lab_test():
    try:
        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        query = {"$or": [{database_constants.LAB_STATUS: constants.CREATED},
                         {database_constants.LAB_STATUS: constants.COMPLETED}]}
        lab_data_points = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_LAB, query)
        results = []
        msg = ""
        for data in lab_data_points:
            lab_object = {
                database_constants.LAB_ID: data[database_constants.LAB_ID],
                database_constants.LAB_USER_ID: data[database_constants.LAB_USER_ID],
                database_constants.LAB_DOCTOR_ID: data[database_constants.LAB_DOCTOR_ID],
                database_constants.LAB_DIAGNOSIS_ID: data[database_constants.LAB_DIAGNOSIS_ID],
                database_constants.LAB_USER_EMAIL: cryptograpy_api.decode(data[database_constants.LAB_USER_EMAIL]),
                database_constants.LAB_DOCTOR_EMAIL: cryptograpy_api.decode(data[database_constants.LAB_DOCTOR_EMAIL]),
                database_constants.LAB_APPOINTMENT_ID: data[database_constants.LAB_APPOINTMENT_ID],
                database_constants.LAB_STATUS: data[database_constants.LAB_STATUS],
                database_constants.LAB_REPORT: cryptograpy_api.decode(data[database_constants.LAB_REPORT]),
                database_constants.LAB_TEST: cryptograpy_api.decode(data[database_constants.LAB_TEST])
            }

            results.append(lab_object)

        if len(results) == 0:
            msg = constants.MESSAGE_NO_LAB_REPORT_REQUEST_PENDING

        mongo_client.close()

        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.DATA: results,
            constants.MESSAGE: msg
        }

        return response
    except Exception as e:
        logging.error("Application: create_diagnosis_report() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def get_lab_record_by_appointment_id(post_data):
    """
        This API Updates patient Full name and date of birth

        Args: post_data which has values of Doctor full name and date of birth which can be updated to DB.

        Returns : response message with success or fail status
    """
    try:
        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        query = {database_constants.LAB_APPOINTMENT_ID: post_data[database_constants.LAB_APPOINTMENT_ID]}

        lab_record = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_LAB, query)
        records = defaultdict(str)
        msg = constants.MESSAGE_NO_LAB_RECORDS_FOUND
        for data in lab_record:
            records = {
                database_constants.LAB_ID: data[database_constants.LAB_ID],
                database_constants.LAB_USER_ID: data[database_constants.LAB_USER_ID],
                database_constants.LAB_DOCTOR_ID: data[database_constants.LAB_DOCTOR_ID],
                database_constants.LAB_DIAGNOSIS_ID: data[database_constants.LAB_DIAGNOSIS_ID],
                database_constants.LAB_USER_EMAIL: cryptograpy_api.decode(data[database_constants.LAB_USER_EMAIL]),
                database_constants.LAB_DOCTOR_EMAIL: cryptograpy_api.decode(data[database_constants.LAB_DOCTOR_EMAIL]),
                database_constants.LAB_APPOINTMENT_ID: data[database_constants.LAB_APPOINTMENT_ID],
                database_constants.LAB_TEST: cryptograpy_api.decode(data[database_constants.LAB_TEST]),
                database_constants.LAB_REPORT: cryptograpy_api.decode(data[database_constants.LAB_REPORT])
            }
            msg = ""

        mongo_client.close()
        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.DATA: records,
            constants.MESSAGE: msg
        }

        return response
    except Exception as e:
        logging.error("Application: get_lab_record_by_appointment_id() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def create_update_lab_report(post_data):
    """
        This API Updates patient Full name and date of birth

        Args: post_data which has values of Doctor full name and date of birth which can be updated to DB.

        Returns : response message with success or fail status
    """
    try:
        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        query = {database_constants.LAB_APPOINTMENT_ID: post_data[database_constants.LAB_APPOINTMENT_ID]}
        current_time = datetime.today()
        date_time_string = current_time.strftime("%m/%d/%Y, %H:%M:%S")
        current_time = current_time.isoformat()

        new_value = {"$set": {database_constants.LAB_REPORT: cryptograpy_api.encode(
            post_data[database_constants.LAB_REPORT]),
            database_constants.LAB_DATE: current_time, database_constants.LAB_TIME: date_time_string,
            database_constants.LAB_STATUS: constants.COMPLETED}}

        mongo_db_api.update_one_into_db(mongo_client=mongo_client, database_name=constants.DATABASE_HMS,
                                        collection_name=constants.COLLECTION_LAB, filter_query=query,
                                        new_value=new_value)

        mongo_client.close()
        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.MESSAGE: constants.MESSAGE_CREATED_UPDATED_LAB_RECORD
        }
        return response
    except Exception as e:
        logging.error("Application: create_update_lab_report() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def delete_lab_report(post_data):
    """
        This API Updates patient Full name and date of birth

        Args: post_data which has values of Doctor full name and date of birth which can be updated to DB.

        Returns : response message with success or fail status
    """
    try:
        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        query = {database_constants.LAB_ID: post_data[database_constants.LAB_ID]}

        count = mongo_db_api.count_document_in_search_query(mongo_client, constants.DATABASE_HMS,
                                                            constants.COLLECTION_LAB, query)

        if count == 0:
            response = {
                constants.STATUS: constants.STATUS_FAILURE,
                constants.MESSAGE: constants.MESSAGE_NO_LAB_RECORDS_FOUND_WITH_RECORD_ID
            }
            return response

        data = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_LAB, query)

        diagnosis_id = data[0][database_constants.LAB_DIAGNOSIS_ID]
        diagnosis_query = {database_constants.DIAGNOSIS_ID: diagnosis_id}
        new_value = {"$set": {database_constants.LAB_ID: "Deleted Lab Record by Lab Staff"}}

        mongo_db_api.update_one_into_db(mongo_client=mongo_client, database_name=constants.DATABASE_HMS,
                                        collection_name=constants.COLLECTION_DIAGNOSIS, filter_query=diagnosis_query,
                                        new_value=new_value)

        mongo_db_api.delete_one_document(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_LAB, query)
        mongo_client.close()
        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.MESSAGE: constants.MESSAGE_DELETED_LAB_RECORD_SUCCESSFULLY
        }

        return response
    except Exception as e:
        logging.error("Application: delete_lab_report() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e