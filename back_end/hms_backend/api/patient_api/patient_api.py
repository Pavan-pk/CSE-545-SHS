import logging
import traceback
from datetime import datetime, timedelta
from hms_backend.api.authorization_api import cryptograpy_api
from hms_backend.databases import mongo_db_api
from hms_backend.project_constants import constants, database_constants


def get_user_data(user_data):
    """
        This API gets complete patient info/details from DB

        Returns: Response with Patient profile data.
    """
    try:
        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        query = {"$and": [
            {database_constants.USER_HASH_EMAIL: cryptograpy_api.hash_encode(user_data[database_constants.USER_EMAIL])},
            {database_constants.USER_USER_TYPE: user_data[database_constants.USER_USER_TYPE]}]}
        required_column = {"_id": 0}
        data = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_USERS, query,
                                      required_column)

        patient_data = {
            database_constants.USER_USER_ID: data[0][database_constants.USER_USER_ID],
            database_constants.USER_FULL_NAME: cryptograpy_api.decode(data[0][database_constants.USER_FULL_NAME]),
            database_constants.USER_BIRTH_DATE: data[0][database_constants.USER_BIRTH_DATE],
            database_constants.USER_EMAIL: user_data[database_constants.USER_EMAIL],
            database_constants.USER_USER_TYPE: user_data[database_constants.USER_USER_TYPE],
            database_constants.USER_SPECIALITY: data[0][database_constants.USER_SPECIALITY]
        }

        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.DATA: patient_data
        }

        return response
    except Exception as e:
        logging.error("Application: get_user_data() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def update_patient_info(post_data):
    """
        This API Updates patient Full name and date of birth

        Args: post_data which has values of Patient full name and date of birth which can be updated to DB.

        Returns : response message with success or fail status
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

        new_value = {"$set": {database_constants.USER_FULL_NAME: cryptograpy_api.encode(
            post_data[database_constants.USER_FULL_NAME]),
            database_constants.USER_BIRTH_DATE: post_data[database_constants.USER_BIRTH_DATE],
            database_constants.USER_SPECIALITY: post_data[database_constants.USER_SPECIALITY]}}

        mongo_db_api.update_one_into_db(mongo_client=mongo_client, database_name=constants.DATABASE_HMS,
                                        collection_name=constants.COLLECTION_USERS, filter_query=query,
                                        new_value=new_value)
        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.MESSAGE: constants.MESSAGE_USER_INFO_UPDATED
        }
        mongo_client.close()
        return response
    except Exception as e:
        logging.error("Application: update_patient_info() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def get_appointment_data():
    """
        This API gets complete patient info/details from DB

        Returns: Response with Patient profile data.
    """
    try:
        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        current_date = datetime.today() + timedelta(minutes=60)
        day = int(current_date.strftime("%d"))
        month = int(current_date.strftime("%m"))
        year = int(current_date.strftime("%Y"))
        hour = int(current_date.strftime("%H"))
        minute = int(current_date.strftime("%M"))
        current_date = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=0).isoformat()

        future_date = datetime.today() + timedelta(days=2)
        day = int(future_date.strftime("%d"))
        month = int(future_date.strftime("%m"))
        year = int(future_date.strftime("%Y"))
        hour = int(future_date.strftime("%H"))
        minute = int(future_date.strftime("%M"))
        future_date = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=0).isoformat()

        query = {"$and": [{database_constants.APPOINTMENT_DATE: {"$gte": current_date}},
                          {database_constants.APPOINTMENT_DATE: {"$lt": future_date}},
                          {database_constants.APPOINTMENT_STATUS: constants.AVAILABLE}]}
        appointment_data_points = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS,
                                                         constants.COLLECTION_APPOINTMENTS, query)

        results = []
        msg = ""
        for data in appointment_data_points:
            appointment_data = {
                database_constants.APPOINTMENT_APPOINTMENT_ID: data[database_constants.APPOINTMENT_APPOINTMENT_ID],
                database_constants.APPOINTMENT_TIME: data[database_constants.APPOINTMENT_TIME],
                database_constants.APPOINTMENT_DOCTOR_ID: data[database_constants.APPOINTMENT_DOCTOR_ID],
                database_constants.APPOINTMENT_DOCTOR_NAME: cryptograpy_api.decode(data[database_constants.
                                                                                   APPOINTMENT_DOCTOR_NAME]),
                database_constants.APPOINTMENT_DOCTOR_EMAIL: cryptograpy_api.decode(data[database_constants.
                                                                                    APPOINTMENT_DOCTOR_EMAIL]),
                database_constants.APPOINTMENT_DOCTOR_SPECIALITY: data[database_constants.APPOINTMENT_DOCTOR_SPECIALITY]
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


def book_general_appointment(post_data):
    """
        This API gets complete patient info/details from DB

        Returns: Response with Patient profile data.
    """
    try:
        appointment_id = post_data[database_constants.APPOINTMENT_APPOINTMENT_ID]

        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        query = {"$and": [{database_constants.APPOINTMENT_APPOINTMENT_ID: appointment_id},
                          {database_constants.APPOINTMENT_STATUS: constants.AVAILABLE}]}

        count = mongo_db_api.count_document_in_search_query(mongo_client, constants.DATABASE_HMS,
                                                            constants.COLLECTION_APPOINTMENTS, query)

        if count == 0:
            response = {
                constants.STATUS: constants.STATUS_FAILURE,
                constants.MESSAGE: constants.MESSAGE_SLOT_NOT_AVAILABLE
            }
            return response

        new_value = {"$set": {
            database_constants.APPOINTMENT_USER_ID: post_data[database_constants.APPOINTMENT_USER_ID],
            database_constants.APPOINTMENT_USER_EMAIL: cryptograpy_api.encode
            (post_data[database_constants.APPOINTMENT_USER_EMAIL]),
            database_constants.APPOINTMENT_STATUS: constants.REQUEST_APPOINTMENT,
        }}

        mongo_db_api.update_one_into_db(mongo_client=mongo_client, database_name=constants.DATABASE_HMS,
                                        collection_name=constants.COLLECTION_APPOINTMENTS, filter_query=query,
                                        new_value=new_value)

        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.MESSAGE: constants.MESSAGE_APPOINTMENT_BOOKED_SUCCESSFULLY
        }
        mongo_client.close()
        return response
    except Exception as e:
        raise e


def cancel_general_appointment(post_data):
    """
        This API gets complete patient info/details from DB

        Returns: Response with Patient profile data.
    """
    try:
        appointment_id = post_data[database_constants.APPOINTMENT_APPOINTMENT_ID]

        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        query = {"$and": [{database_constants.APPOINTMENT_APPOINTMENT_ID: appointment_id}]}

        count = mongo_db_api.count_document_in_search_query(mongo_client, constants.DATABASE_HMS,
                                                            constants.COLLECTION_APPOINTMENTS, query)

        if count == 0:
            response = {
                constants.STATUS: constants.STATUS_FAILURE,
                constants.MESSAGE: constants.MESSAGE_SLOT_NOT_AVAILABLE
            }
            return response

        new_value = {"$set": {
            database_constants.APPOINTMENT_APPOINTMENT_ID: appointment_id,
            database_constants.APPOINTMENT_STATUS: constants.AVAILABLE,
        }}

        mongo_db_api.update_one_into_db(mongo_client=mongo_client, database_name=constants.DATABASE_HMS,
                                        collection_name=constants.COLLECTION_APPOINTMENTS, filter_query=query,
                                        new_value=new_value)

        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.MESSAGE: constants.MESSAGE_APPOINTMENT_CANCELLED_SUCCESSFULLY
        }
        mongo_client.close()
        return response
    except Exception as e:
        raise e


def get_user_details(post_data):
    """
    Args:
        post_data: user_id

    Returns:
        User data
    """
    mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
    try:
        query = {"$and": [
            {database_constants.USER_HASH_EMAIL: cryptograpy_api.hash_encode(post_data[database_constants.USER_EMAIL])}]}
        required_column = {"_id": 0}
        data = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_USERS, query,
                                      required_column)

        patient_data = {
            database_constants.USER_USER_ID: data[0][database_constants.USER_USER_ID],
            database_constants.USER_FULL_NAME: cryptograpy_api.decode(data[0][database_constants.USER_FULL_NAME]),
            database_constants.USER_BIRTH_DATE: data[0][database_constants.USER_BIRTH_DATE],
            database_constants.USER_EMAIL: cryptograpy_api.decode(data[0][database_constants.USER_EMAIL]),
            database_constants.USER_USER_TYPE: data[0][database_constants.USER_USER_TYPE],
            database_constants.USER_SPECIALITY: data[0][database_constants.USER_SPECIALITY]
        }

        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.DATA: patient_data
        }
        return response
    except Exception as e:
        logging.error("Application: get_user_data() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e
    finally:
        mongo_client.close()


def get_transactions(user_data):
    mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
    try:
        query = {database_constants.USER_USER_ID: user_data[database_constants.USER_USER_ID]}
        transactions = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS,
                                                         constants.COLLECTION_TRANSACTION, query)

        results = []
        for data in transactions:
            appointment_data = {
                database_constants.TRANSACTION_ID: data[database_constants.TRANSACTION_ID],
                database_constants.TRANSACTION_APPOINTMENT_ID: data[database_constants.TRANSACTION_DETAILS][database_constants.TRANSACTION_APPOINTMENT_ID],
                database_constants.TRANSACTION_REASON: data[database_constants.TRANSACTION_DETAILS][database_constants.TRANSACTION_REASON],
                database_constants.TRANSACTION_AMOUNT: data[database_constants.TRANSACTION_DETAILS][database_constants.TRANSACTION_AMOUNT],
                database_constants.TRANSACTION_TYPE: data[database_constants.TRANSACTION_TYPE],
                database_constants.TRANSACTION_STATUS: data[database_constants.USER_USER_TYPE]
            }
            results.append(appointment_data)

        if len(results) == 0:
            msg = constants.MESSAGE_NO_TRANSACTIONS_AVAILABLE
        else:
            msg = constants.MESSAGE_TRANSACTIONS_RETRIEVED
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


def get_medical_records(post_data):
    try:
        user_id = post_data[database_constants.USER_USER_ID]

        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        query = {database_constants.USER_USER_ID: user_id}

        diagnosis_data = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_DIAGNOSIS,
                                                query)
        lab_query = {"$and": [{database_constants.USER_USER_ID: user_id}, {database_constants.LAB_STATUS: constants.COMPLETED}]}
        lab_data = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS, constants.COLLECTION_LAB, lab_query)

        prescription_data = mongo_db_api.search_db(mongo_client, constants.DATABASE_HMS,
                                                   constants.COLLECTION_PRESCRIPTION, query)

        diagnosis_result = []
        for data in diagnosis_data:
            diagnosis_object = {
                database_constants.DIAGNOSIS_ID: data[database_constants.DIAGNOSIS_ID],
                database_constants.DIAGNOSIS_RECORD: cryptograpy_api.decode(data[database_constants.DIAGNOSIS_RECORD]),
                database_constants.DIAGNOSIS_TIME: data[database_constants.DIAGNOSIS_TIME]
            }
            diagnosis_result.append(diagnosis_object)

        lab_records = []
        for data in lab_data:
            lab_object = {
                database_constants.LAB_ID: data[database_constants.LAB_ID],
                database_constants.LAB_TEST: cryptograpy_api.decode(data[database_constants.LAB_TEST]),
                database_constants.LAB_TIME: data[database_constants.LAB_TIME],
                database_constants.LAB_REPORT: cryptograpy_api.decode(data[database_constants.LAB_REPORT])
            }

            lab_records.append(lab_object)

        prescription_record = []

        for data in prescription_data:
            prescription_object = {
                database_constants.PRESCRIPTION_ID: data[database_constants.PRESCRIPTION_ID],
                database_constants.PRESCRIPTION_RECORD: cryptograpy_api.decode(data[database_constants.PRESCRIPTION_RECORD]),
                database_constants.PRESCRIPTION_TIME: data[database_constants.PRESCRIPTION_TIME],
            }

            prescription_record.append(prescription_object)

        msg = constants.MESSAGE_MEDICAL_DATA_FOUND

        if len(diagnosis_result) == 0 and len(prescription_record) == 0 and len(lab_records) == 0:
            msg = constants.MESSAGE_NO_MEDICAL_DATA_FOUND

        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.DIAGNOSIS_DATA: diagnosis_result,
            constants.PRESCRIPTION_DATA: prescription_record,
            constants.LAB_DATA: lab_records,
            constants.MESSAGE: msg
        }

        mongo_client.close()
        return response
    except Exception as e:
        raise e
