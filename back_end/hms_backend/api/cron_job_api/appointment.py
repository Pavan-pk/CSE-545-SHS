import pymongo
import time
from datetime import date, datetime, timedelta
import hashlib
from cryptography.fernet import Fernet
from hms_backend.project_constants import constants
from flask import current_app as app


# key for encoding and decoding data-field is fixed.
# key itself is encoded to bytes & passed to Fernet object.
def encode(data):
    """
        API to do field level encryption of the database.

        Args:
            data (str): Data to encrypt

        Return:
            Encrypted Data
    """
    fernet = Fernet("mchnf614q9jEJUV5UXiuS-qS14Rg8Gqwu7tRUHyj0T4=")
    return fernet.encrypt(data.encode())


def decode(encrypted_data):
    """
        API to do field level decryption of the database.

        Args:
            encrypted_data (str): Data to decrypt

        Return:
            Decrypted Data
    """
    fernet = Fernet("mchnf614q9jEJUV5UXiuS-qS14Rg8Gqwu7tRUHyj0T4=")
    return fernet.decrypt(encrypted_data).decode()


def hash_encode(data):
    """
        API to do one way encryption of the data. Note this data cannot be decrypted.

        Args:
            data (str): Data to encrypt

        Return:
            Encrypted Data
    """
    return hashlib.md5(data.encode()).hexdigest()


def search_db(mongo_client, database_name, collection_name, query):
    """
        Search document in database

        Args:
            mongo_client (str): Mongo client for connecting to Database
            database_name (str): Name of the Database
            collection_name (str): Name of the Collection
            query (str): Database query for easy search

        Return:
             Database Configuration Object
    """
    try:
        database = mongo_client[database_name]
        collection = database[collection_name]
        data = collection.find(query)
        return data
    except Exception as e:
        print(e)


def delete_many_document(mongo_client, database_name, collection_name, query):
    """
        Search document in database

        Args:
            mongo_client (str): Mongo client for connecting to Database
            database_name (str): Name of the Database
            collection_name (str): Name of the Collection
            query (str): Database query for easy search

        Return:
             Database Configuration Object
    """
    try:
        database = mongo_client[database_name]
        collection = database[collection_name]
        count = collection.delete_many(query)
        return count
    except Exception as e:
        print(e)


def insert_one_into_db(mongo_client, database_name, collection_name, data):
    """
        Insert one document in the collection.

        Args:
            mongo_client (str): Mongo client for connecting to Database
            database_name (str): Name of the Database
            collection_name (str): Name of the Collection
            data (str): Document data that needs to be inserted in the collection

        Return:
             Database Configuration Object
    """
    try:
        database = mongo_client[database_name]
        collection = database[collection_name]
        collection.insert_one(data)
    except Exception as e:
        print(e)


def get_next_sequence(mongo_client, database_name, collection_name, name):
    """
        Create MongoDB client from configuration object.

        Args:
            mongo_client (str): Mongo client for connecting to Database
            database_name (str): Name of the Database
            collection_name (str): Name of the Collection
            name (str): Name of the Column for which auto sequence need to be generated
        Return:
             Database Configuration Object
    """
    try:
        database = mongo_client[database_name]
        collection = database[collection_name]
        data = collection.find_and_modify(
            query={"Name": name},
            update={"$inc": {"Value": 1}},
            new=True,
            upsert=True
        )
        return data["Value"]
    except Exception as e:
        print(e)


def get_database_client():
    """
        Create MongoDB client from configuration object.

        Return:
             Database Configuration Object
    """
    try:
        user_name = "websitewriter"
        password = "iliketowrite#ss#2022"
        host_name = "ec2-54-201-199-55.us-west-2.compute.amazonaws.com"
        port = "27017"
        auth_source = "admin"
        database_name = "HotelManagementSystem"
        connection_url = "mongodb://" + user_name + ":" + password + "@" + host_name + ":" + port + "/" + \
                         database_name + "?authSource=" + auth_source
        return pymongo.MongoClient(connection_url)
    except Exception as e:
        raise e


def get_all_doctors():
    client = get_database_client()
    database = "HotelManagementSystem"
    collection = "users"
    query = {"user_type": "3"}
    data = search_db(client, database, collection, query)
    list_of_doctor = []
    for data_point in data:
        temp_data = {
            "doctor_id": data_point["user_id"],
            "doctor_name": data_point["full_name"],
            "doctor_email": data_point["email"],
            "doctor_speciality": data_point["user_speciality"]
        }

        list_of_doctor.append(temp_data)

    return list_of_doctor


def add_appointments(doctors_list, book_date):
    try:
        client = get_database_client()
        database = "HotelManagementSystem"
        collection = "appointments"
        future_date = datetime.today() + timedelta(book_date)
        day = int(future_date.strftime("%d"))
        month = int(future_date.strftime("%m"))
        year = int(future_date.strftime("%Y"))
        current_date = date.today() + timedelta(book_date)
        end_date = current_date.strftime("%d %b %Y")
        delta = "AM"
        for i in range(0, 24):
            curr_time = str(i % 12)
            if i != 0 and i % 12 == 0:
                delta = "PM"
                curr_time = str(12)

            first = datetime(year=year, month=month, day=day, hour=i, minute=0, second=0, microsecond=0).isoformat()
            first_time = end_date + ", " + curr_time + ":00" + delta + " to " + curr_time + ":29" + delta

            second = datetime(year=year, month=month, day=day, hour=i, minute=30, second=0, microsecond=0).isoformat()
            second_time = end_date + ", " + curr_time + ":30" + delta + " to " + curr_time + ":59" + delta

            for doctor_data in doctors_list:
                appointment_id = get_next_sequence(client, database, collection, "appointment_id")
                appointment_data = {
                    "appointment_id": str(appointment_id),
                    "date": first,
                    "time": first_time,
                    "user_id": "",
                    "user_email": "",
                    "doctor_id": doctor_data["doctor_id"],
                    "doctor_name": doctor_data["doctor_name"],
                    "doctor_email": doctor_data["doctor_email"],
                    "doctor_speciality": doctor_data["doctor_speciality"],
                    "status": "Available"
                }

                insert_one_into_db(client, database, collection, appointment_data)
                appointment_id_1 = get_next_sequence(client, database, collection, "appointment_id")
                appointment_data_2 = {
                    "appointment_id": str(appointment_id_1),
                    "date": second,
                    "time": second_time,
                    "user_id": "",
                    "user_email": "",
                    "doctor_id": doctor_data["doctor_id"],
                    "doctor_name": doctor_data["doctor_name"],
                    "doctor_email": doctor_data["doctor_email"],
                    "doctor_speciality": doctor_data["doctor_speciality"],
                    "status": "Available"
                }
                insert_one_into_db(client, database, collection, appointment_data_2)

        client.close()
    except Exception as e:
        print(e)


def delete_appointment():
    try:
        client = get_database_client()
        database = "HotelManagementSystem"
        collection = "appointments"
        current_date = datetime.today()
        day = int(current_date.strftime("%d"))
        month = int(current_date.strftime("%m"))
        year = int(current_date.strftime("%Y"))

        current_date = datetime(year=year, month=month, day=day, hour=0, minute=0, second=0, microsecond=0).isoformat()
        query = {"$and": [{"status": "Available"}, {"date": {"$lt": current_date}}]}
        delete_many_document(client, database, collection, query)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    list_of_doctor = get_all_doctors()
    for app in range(1, 2):
        add_appointments(list_of_doctor, app)
    delete_appointment()
