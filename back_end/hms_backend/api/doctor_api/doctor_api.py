import logging
import traceback
from datetime import datetime
from hms_backend.api.authorization_api import cryptograpy_api
from hms_backend.databases import mongo_db_api
from hms_backend.project_constants import constants, database_constants
from collections import defaultdict


def get_current_appointment_details(post_data):
    try:
        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        current_time = datetime.today()
        day = int(current_time.strftime("%d"))
        month = int(current_time.strftime("%m"))
        year = int(current_time.strftime("%Y"))
        hour = int(current_time.strftime("%H"))
        minute = int(current_time.strftime("%M"))

        if minute >= 30:
            past_time = datetime(year=year, month=month, day=day, hour=hour, minute=30, second=0).isoformat()
            future_time = datetime(year=year, month=month, day=day, hour=hour + 1, minute=0, second=0).isoformat()
        else:
            past_time = datetime(year=year, month=month, day=day, hour=hour, minute=0, second=0).isoformat()
            future_time = datetime(year=year, month=month, day=day, hour=hour, minute=30, second=0).isoformat()

        query = {
            "$and": [{database_constants.APPOINTMENT_DOCTOR_ID: post_data[database_constants.APPOINTMENT_DOCTOR_ID]},
                     {database_constants.APPOINTMENT_DATE: {"$gte": past_time}},
                     {database_constants.APPOINTMENT_DATE: {"$lt": future_time}},
                     {database_constants.APPOINTMENT_STATUS: constants.BOOKED}]}
        appointment_data_points = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS,
                                                         constants.COLLECTION_APPOINTMENTS, query)

        results = []
        msg = ""
        for data in appointment_data_points:
            appointment_data = {
                database_constants.APPOINTMENT_APPOINTMENT_ID: data[database_constants.APPOINTMENT_APPOINTMENT_ID],
                database_constants.APPOINTMENT_TIME: data[database_constants.APPOINTMENT_TIME],
                database_constants.APPOINTMENT_DOCTOR_ID: data[database_constants.APPOINTMENT_DOCTOR_ID],
                database_constants.APPOINTMENT_USER_ID: data[database_constants.APPOINTMENT_USER_ID],
                database_constants.APPOINTMENT_USER_EMAIL: data[database_constants.APPOINTMENT_USER_EMAIL],
                database_constants.APPOINTMENT_DOCTOR_NAME:
                    cryptograpy_api.decode(data[database_constants.APPOINTMENT_DOCTOR_NAME]),
                database_constants.APPOINTMENT_DOCTOR_EMAIL:
                    cryptograpy_api.decode(data[database_constants.APPOINTMENT_DOCTOR_EMAIL]),
                database_constants.APPOINTMENT_DOCTOR_SPECIALITY: data[
                    database_constants.APPOINTMENT_DOCTOR_SPECIALITY],
            }
            results.append(appointment_data)

        if len(results) == 0:
            msg = constants.MESSAGE_NO_CURRENT_APPOINTMENT

        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.DATA: results[-1] if results else {},
            constants.MESSAGE: msg
        }

        return response
    except Exception as e:
        logging.error("Application: update_patient_info() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def create_diagnosis_report(post_data):
    """
        This API Updates patient Full name and date of birth

        Args: post_data which has values of Doctor full name and date of birth which can be updated to DB.

        Returns : response message with success or fail status
    """
    try:
        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        query = {"$and": [
            {database_constants.DIAGNOSIS_DOCTOR_ID: post_data[database_constants.DIAGNOSIS_DOCTOR_ID],
             database_constants.APPOINTMENT_APPOINTMENT_ID: post_data[database_constants.APPOINTMENT_APPOINTMENT_ID]}]}

        count = mongo_db_api.count_document_in_search_query(mongo_client, constants.DATABASE_HMS,
                                                            constants.COLLECTION_DIAGNOSIS, query)
        if count:
            return update_diagnosis_report(post_data)

        diagnosis_id = mongo_db_api.get_next_sequence(mongo_client, constants.DATABASE_HMS,
                                                      constants.COLLECTION_DIAGNOSIS, database_constants.DIAGNOSIS_ID)

        lab_id = mongo_db_api.get_next_sequence(mongo_client, constants.DATABASE_HMS,
                                                constants.COLLECTION_LAB, database_constants.LAB_ID)

        prescription_id = mongo_db_api.get_next_sequence(mongo_client, constants.DATABASE_HMS,
                                                         constants.COLLECTION_PRESCRIPTION,
                                                         database_constants.PRESCRIPTION_ID)

        current_time = datetime.today()
        date_time_string = current_time.strftime("%m/%d/%Y, %H:%M:%S")
        current_time = current_time.isoformat()
        diagnosis_object = {
            database_constants.DIAGNOSIS_ID: str(diagnosis_id),
            database_constants.DIAGNOSIS_PRESCRIPTION_ID: str(prescription_id),
            database_constants.DIAGNOSIS_LAB_ID: str(lab_id),
            database_constants.DIAGNOSIS_USER_ID: post_data[database_constants.DIAGNOSIS_USER_ID],
            database_constants.DIAGNOSIS_USER_EMAIL: cryptograpy_api.encode(post_data
                                                                            [database_constants.DIAGNOSIS_USER_EMAIL]),
            database_constants.DIAGNOSIS_DOCTOR_ID: post_data[database_constants.DIAGNOSIS_DOCTOR_ID],
            database_constants.DIAGNOSIS_DOCTOR_NAME: cryptograpy_api.encode(
                post_data[database_constants.DIAGNOSIS_DOCTOR_NAME]),
            database_constants.DIAGNOSIS_DOCTOR_EMAIL: cryptograpy_api.encode(
                post_data[database_constants.DIAGNOSIS_DOCTOR_EMAIL]),
            database_constants.DIAGNOSIS_RECORD: cryptograpy_api.encode(post_data[database_constants.DIAGNOSIS_RECORD]),
            database_constants.DIAGNOSIS_APPOINTMENT_ID: post_data[database_constants.DIAGNOSIS_APPOINTMENT_ID],
            database_constants.DIAGNOSIS_DATE: current_time,
            database_constants.DIAGNOSIS_TIME: date_time_string,
            database_constants.DIAGNOSIS_STATUS: constants.CREATED
        }

        lab_object = {
            database_constants.LAB_ID: str(lab_id),
            database_constants.LAB_USER_ID: post_data[database_constants.LAB_USER_ID],
            database_constants.LAB_DOCTOR_ID: post_data[database_constants.LAB_DOCTOR_ID],
            database_constants.LAB_DIAGNOSIS_ID: str(diagnosis_id),
            database_constants.LAB_USER_EMAIL: cryptograpy_api.encode(post_data[
                                                                          database_constants.LAB_USER_EMAIL]),
            database_constants.LAB_DOCTOR_EMAIL: cryptograpy_api.encode(post_data[database_constants.LAB_DOCTOR_EMAIL]),
            database_constants.LAB_APPOINTMENT_ID: post_data[database_constants.LAB_APPOINTMENT_ID],
            database_constants.LAB_TEST: cryptograpy_api.encode(post_data[database_constants.LAB_TEST]),
            database_constants.LAB_DATE: current_time,
            database_constants.LAB_TIME: date_time_string,
            database_constants.LAB_REPORT: cryptograpy_api.encode(""),
            database_constants.LAB_STATUS: constants.CREATED,
        }

        prescription_object = {
            database_constants.PRESCRIPTION_ID: str(prescription_id),
            database_constants.PRESCRIPTION_USER_ID: post_data[database_constants.PRESCRIPTION_USER_ID],
            database_constants.PRESCRIPTION_DOCTOR_ID: post_data[database_constants.PRESCRIPTION_DOCTOR_ID],
            database_constants.PRESCRIPTION_DIAGNOSIS_ID: str(diagnosis_id),
            database_constants.PRESCRIPTION_USER_EMAIL: cryptograpy_api.encode(
                post_data[database_constants.PRESCRIPTION_USER_EMAIL]),
            database_constants.PRESCRIPTION_DOCTOR_EMAIL: cryptograpy_api.encode(
                post_data[database_constants.PRESCRIPTION_DOCTOR_EMAIL]),
            database_constants.PRESCRIPTION_APPOINTMENT_ID: post_data[database_constants.PRESCRIPTION_APPOINTMENT_ID],
            database_constants.PRESCRIPTION_RECORD: cryptograpy_api.encode(
                post_data[database_constants.PRESCRIPTION_RECORD]),
            database_constants.PRESCRIPTION_DATE: current_time,
            database_constants.PRESCRIPTION_TIME: date_time_string,
            database_constants.PRESCRIPTION_STATUS: constants.CREATED,
        }

        mongo_db_api.insert_one_into_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_DIAGNOSIS,
                                        diagnosis_object)

        mongo_db_api.insert_one_into_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_LAB,
                                        lab_object)

        mongo_db_api.insert_one_into_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_PRESCRIPTION,
                                        prescription_object)

        mongo_client.close()
        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.MESSAGE: constants.MESSAGE_DIAGNOSIS_ADDED
        }
        return response
    except Exception as e:
        logging.error("Application: create_diagnosis_report() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def get_diagnosis_report(post_data):
    """
        This API Updates patient Full name and date of birth

        Args: post_data which has values of Doctor full name and date of birth which can be updated to DB.

        Returns : response message with success or fail status
    """
    try:
        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        query = {"$and": [
            {database_constants.DIAGNOSIS_DOCTOR_ID: post_data[database_constants.DIAGNOSIS_DOCTOR_ID],
             database_constants.APPOINTMENT_APPOINTMENT_ID: post_data[database_constants.APPOINTMENT_APPOINTMENT_ID]}]}

        diagnosis = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_DIAGNOSIS, query)
        prescription = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_PRESCRIPTION,
                                              query)
        lab_test = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_LAB, query)

        record_dict = defaultdict(str)
        for diagnosis_data in diagnosis:
            record_dict[database_constants.DIAGNOSIS_RECORD] = \
                cryptograpy_api.decode(diagnosis_data[database_constants.DIAGNOSIS_RECORD])
        for prescription_data in prescription:
            record_dict[database_constants.PRESCRIPTION_RECORD] = \
                cryptograpy_api.decode(prescription_data[database_constants.PRESCRIPTION_RECORD])
        for lab_data in lab_test:
            record_dict[database_constants.LAB_TEST] = \
                cryptograpy_api.decode(lab_data[database_constants.LAB_TEST])

        mongo_client.close()
        msg = constants.MESSAGE_NO_DIAGNOSIS_RECORDS_FOUND

        if len(record_dict) != 0:
            msg = ""
        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.DATA: record_dict,
            constants.MESSAGE: msg
        }
        return response
    except Exception as e:
        logging.error("Application: create_diagnosis_report() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def update_diagnosis_report(post_data):
    """
        This API Updates patient Full name and date of birth

        Args: post_data which has values of Doctor full name and date of birth which can be updated to DB.

        Returns : response message with success or fail status
    """
    try:
        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        query = {"$and": [
            {database_constants.DIAGNOSIS_DOCTOR_ID: post_data[database_constants.DIAGNOSIS_DOCTOR_ID],
             database_constants.APPOINTMENT_APPOINTMENT_ID: post_data[database_constants.APPOINTMENT_APPOINTMENT_ID]}]}

        new_value = {"$set": {database_constants.PRESCRIPTION_RECORD: cryptograpy_api.encode(
            post_data[database_constants.PRESCRIPTION_RECORD])}}
        mongo_db_api.update_one_into_db(mongo_client=mongo_client, database_name=constants.DATABASE_HMS,
                                        collection_name=constants.COLLECTION_PRESCRIPTION, filter_query=query,
                                        new_value=new_value)
        new_value = {"$set": {database_constants.LAB_TEST: cryptograpy_api.encode(
            post_data[database_constants.LAB_TEST])}}
        mongo_db_api.update_one_into_db(mongo_client=mongo_client, database_name=constants.DATABASE_HMS,
                                        collection_name=constants.COLLECTION_LAB, filter_query=query,
                                        new_value=new_value)
        new_value = {"$set": {database_constants.DIAGNOSIS_RECORD: cryptograpy_api.encode(
            post_data[database_constants.DIAGNOSIS_RECORD])}}
        mongo_db_api.update_one_into_db(mongo_client=mongo_client, database_name=constants.DATABASE_HMS,
                                        collection_name=constants.COLLECTION_DIAGNOSIS, filter_query=query,
                                        new_value=new_value)
        mongo_client.close()
        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.MESSAGE: constants.MESSAGE_DIAGNOSIS_UPDATED
        }
        return response
    except Exception as e:
        logging.error("Application: create_diagnosis_report() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e
