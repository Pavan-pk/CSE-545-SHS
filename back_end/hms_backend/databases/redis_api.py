import logging
import traceback
from hms_backend.api.authorization_api import cryptograpy_api
from datetime import timedelta


def insert_into_redis(redis_client, key, extended_key, value, expiry_timer):
    try:
        final_key = key + extended_key
        encode_key = cryptograpy_api.hash_encode(final_key)
        encode_value = cryptograpy_api.encode(value)
        redis_client.set(encode_key, encode_value)
        redis_client.expire(encode_key, timedelta(minutes=expiry_timer))
    except Exception as e:
        logging.error("Application: insert_into_redis() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e


def get_from_redis(redis_client, key, extended_key):
    try:
        final_key = key + extended_key
        encode_key = cryptograpy_api.hash_encode(final_key)
        value = redis_client.get(encode_key)
        if value is not None:
            return cryptograpy_api.decode(value)
        return None
    except Exception as e:
        logging.error("Application: get_from_redis() issue: " + str(e) + "\n" + traceback.format_exc())
        raise e
