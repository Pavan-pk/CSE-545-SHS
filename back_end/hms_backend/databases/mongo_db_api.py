import pymongo
import gridfs
from hms_backend.project_constants import constants
import logging
import traceback
from flask import current_app as app


def get_database_client(database_name):
    """
        Create MongoDB client from configuration object.

        Args:
            database_name (str): Name of the Database

        Return:
             Database Configuration Object
    """
    try:
        user_name = app.config[constants.DB_USER_NAME]
        password = app.config[constants.DB_PASSWORD]
        host_name = app.config[constants.DB_HOST_NAME]
        port = app.config[constants.DB_PORT]
        auth_source = app.config[constants.DB_AUTH_SOURCE]
        connection_url = "mongodb://" + user_name + ":" + password + "@" + host_name + ":" + port + "/" + \
                         database_name + "?authSource=" + auth_source

        if app.config[constants.ENVIRONMENT] == constants.ENV_PROD:
            client = pymongo.MongoClient(connection_url, tls=True,
                                         tlsCAFile=app.config[constants.DB_SSL_CERTIFICATE_LOCATION])
        else:
            client = pymongo.MongoClient(connection_url)
        return client
    except Exception as e:
        logging.error("MongoDB get_database_client() Issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


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
        logging.error("MongoDB insert_one_into_db() Issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def update_one_into_db(mongo_client, database_name, collection_name, filter_query, new_value):
    """
        Update one document in the database.

        Args:
            mongo_client (str): Mongo client for connecting to Database
            database_name (str): Name of the Database
            collection_name (str): Name of the Collection
            filter_query (str): Database filter query
            new_value (str): new updated value

        Return:
             Database Configuration Object
    """
    try:
        database = mongo_client[database_name]
        collection = database[collection_name]
        collection.update_one(filter_query, new_value)
    except Exception as e:
        logging.error("MongoDB update_one_into_db() Issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def update_many_into_db(mongo_client, database_name, collection_name, filter_query, new_value):
    """
        Update many document in the database.

        Args:
            mongo_client (str): Mongo client for connecting to Database
            database_name (str): Name of the Database
            collection_name (str): Name of the Collection
            filter_query (str): Database filter query
            new_value (str): New updated value

        Return:
             Database Configuration Object
    """
    try:
        database = mongo_client[database_name]
        collection = database[collection_name]
        collection.update_many(filter_query, new_value)
    except Exception as e:
        logging.error("MongoDB update_one_into_db() Issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def search_db(mongo_client, database_name, collection_name, query, required_column=None):
    """
        Search document in database

        Args:
            mongo_client (str): Mongo client for connecting to Database
            database_name (str): Name of the Database
            collection_name (str): Name of the Collection
            query (str): Database Query for easy search
            required_column (str): Query only for require column
        Return:
             Database Configuration Object
    """
    try:
        database = mongo_client[database_name]
        collection = database[collection_name]
        if required_column is not None:
            data = collection.find(query, required_column)
        else:
            data = collection.find(query)
        return data
    except Exception as e:
        logging.error("MongoDB search_db Issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def count_document_in_search_query(mongo_client, database_name, collection_name, query):
    """
        Count number of document in the given collection.

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
        count = collection.count_documents(query)
        return count
    except Exception as e:
        logging.error("MongoDB count_document_in_search_query: " + str(e) + "\n" + traceback.format_exc())
        raise e


def upload_file_to_gridFS(mongo_client, database_name, file_data, file_name):
    """
        Save file in the Grid File System.

        Args:
            mongo_client (str): Mongo client for connecting to the Database
            database_name (str): Name of the Database
            file_data (str): Binary data of file
            file_name (str): Name of the file

        Return:
             Database Configuration Object
    """
    try:
        fs = gridfs.GridFS(mongo_client[database_name])
        fs.put(file_data.encode(), filename=file_name)
    except Exception as e:
        logging.error("MongoDB upload_file_to_gridFS() Issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def delete_one_document(mongo_client, database_name, collection_name, query):
    """
        Delete document in database

        Args:
            mongo_client (str): Mongo client for connecting to Database
            database_name (str): Name of the Database
            collection_name (str): Name of the Collection
            query (str): Database query for easy search

        Return:
             None
    """
    try:
        database = mongo_client[database_name]
        collection = database[collection_name]
        collection.delete_one(query)
    except Exception as e:
        print(e)


def delete_many_document(mongo_client, database_name, collection_name, query):
    """
        Delete Many documents in database

        Args:
            mongo_client (str): Mongo client for connecting to Database
            database_name (str): Name of the Database
            collection_name (str): Name of the Collection
            query (str): Database query for easy search

        Return:
             Count of deleted documents
    """
    try:
        database = mongo_client[database_name]
        collection = database[collection_name]
        count = collection.delete_many(query)
        return count
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
        logging.error("MongoDB get_next_sequence Issue: " + str(e) + "\n" + traceback.format_exc())
        raise e
