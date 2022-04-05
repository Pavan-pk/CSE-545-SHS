from datetime import timedelta
import socket
import logging
import json
import base64
import traceback
from flask import Flask, jsonify, request, url_for
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_executor import Executor
from functools import wraps
from cachetools import TTLCache
from hms_backend.project_logger import backend_logger
from hms_backend.project_constants import constants, database_constants
from hms_backend.databases import mongo_db_api, redis_api
from hms_backend.configuration import application_config
from hms_backend.api.authorization_api import auth_api, cryptograpy_api
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, get_jwt
from redis import Redis
from hms_backend.api.patient_api import patient_api
from hms_backend.api.insurance_api import insurance_api
from hms_backend.api.doctor_api import doctor_api
from hms_backend.api.admin_api import admin_api
from hms_backend.api.lab_staff_api import lab_api
from hms_backend.api.hospital_staff import hospital_staff_api
from hms_backend.ML.Chatbot.ChatBot import ChatBot
import requests


# Flask Server Configuration
app = Flask(__name__)
app.app_context().push()
CORS(app)
cache = TTLCache(maxsize=256, ttl=3600)

# Check the environment, Dev or Prod
host_name = socket.gethostname()
if host_name == constants.PROD_HOST_NAME:
    app.config[constants.ENVIRONMENT] = constants.ENV_PROD
else:
    app.config[constants.ENVIRONMENT] = constants.ENV_DEV

# Setting application variable
app_config_file = application_config.get_application_configuration()
app.config[constants.DB_HOST_NAME] = app_config_file.get(constants.DB_HOST_NAME)
app.config[constants.DB_PORT] = app_config_file.get(constants.DB_PORT)
app.config[constants.DB_AUTH_SOURCE] = app_config_file.get(constants.DB_AUTH_SOURCE)
app.config[constants.DB_NAME] = app_config_file.get(constants.DB_NAME)
app.config[constants.DB_USER_NAME] = app_config_file.get(constants.DB_USER_NAME)
app.config[constants.DB_PASSWORD] = app_config_file.get(constants.DB_PASSWORD)
app.config[constants.DB_SSL_CERTIFICATE_LOCATION] = app_config_file.get(constants.DB_SSL_CERTIFICATE_LOCATION)
app.config[constants.PUBLIC_RSA_KEY] = app_config_file.get(constants.PUBLIC_RSA_KEY)
app.config[constants.PRIVATE_RSA_KEY] = app_config_file.get(constants.PRIVATE_RSA_KEY)
app.config[constants.EMAIL] = app_config_file.get(constants.EMAIL)
app.config[constants.EMAIL_PASSWORD] = app_config_file.get(constants.EMAIL_PASSWORD)
app.config[constants.URL_GENERATOR_SECRET] = app_config_file.get(constants.URL_GENERATOR_SECRET)
app.config[constants.FERNET_KEY] = app_config_file.get(constants.FERNET_KEY)
app.config[constants.EMAIL_SALT] = app_config_file.get(constants.EMAIL_SALT)
app.config[constants.TOKEN_SECRET_KEY] = app_config_file.get(constants.TOKEN_SECRET_KEY)
app.config[constants.MAIL_SERVER] = 'smtp.gmail.com'
app.config[constants.MAIL_PORT] = 465
app.config[constants.MAIL_USERNAME] = app.config[constants.EMAIL]
app.config[constants.MAIL_PASSWORD] = app.config[constants.EMAIL_PASSWORD]
app.config[constants.MAIL_USE_TLS] = False
app.config[constants.MAIL_USE_SSL] = True
app.config[constants.EXECUTOR_TYPE] = 'thread'
app.config[constants.EXECUTOR_MAX_WORKERS] = constants.MAX_NUMBER_OF_THREAD
app.config[constants.EXECUTOR_PROPAGATE_EXCEPTIONS] = True
app.config[constants.REDIS_HOST] = app_config_file[constants.REDIS_HOST]
app.config[constants.REDIS_PORT] = app_config_file[constants.REDIS_PORT]
app.config[constants.JWT_TOKEN_LOCATION] = ["headers"]
app.config[constants.JWT_SECRET_KEY] = app_config_file[constants.JWT_SECRET_KEY]
app.config[constants.JWT_ACCESS_TOKEN_EXPIRES] = timedelta(minutes=constants.JWT_ACCESS_TOKEN_EXPIRES_TIME_MINUTES)
app.config[constants.BLOCKCHAIN_URL] = app_config_file[constants.BLOCKCHAIN_URL]
app.config[constants.ML_PATH] = app_config_file[constants.ML_PATH]

# Initialize e-mail, jwt, redis and multithreading in application context
mail = Mail(app)
executor = Executor(app)
jwt = JWTManager(app)
redis = Redis(host=app.config[constants.REDIS_HOST], port=app.config[constants.REDIS_PORT])
my_chat_bot = ChatBot()


def token_required(calling_function):
    """
        This method is used to check the validation of the users. It will be used as a session, any request come from
        frontend should have the time base token. Then this method decrypt the token and check if current user session
        is expired or not.

        Args:
            calling_function (function): Wrap the calling function with this method to check user session.
        Return:
            None
    """

    @wraps(calling_function)
    def decorated(*args, **kwargs):
        token = None
        header = request.headers

        if constants.AUTHORIZATION in header:
            token = header[constants.AUTHORIZATION]

        if token is None:
            logging.error("Application: token_required(): token missing")

            return jsonify({'status': 'Failure', 'message': 'Token is missing!'})

        return calling_function(*args, **kwargs)

    return decorated


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload[constants.JSON_TOKEN_IDENTIFIER]
    token_in_redis = redis.get(jti)
    return token_in_redis is not None


def decrypt_secret(secret):
    """
        Decrypt secret and return json containing key, iv, and additional data.

        Args:
            secret (str): encrypted secret json encoded in base64.
        Return:
            Json: Decrypted Json of secret.
    """
    private_rsa_key = app.config[constants.PRIVATE_RSA_KEY]
    private_key = serialization.load_pem_private_key(
        private_rsa_key.encode('utf-8'),
        password=None)
    secret_json = private_key.decrypt(
        base64.b64decode(secret),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return json.loads(secret_json)


def get_route_payload(secret, route, payload):
    """
        Given the shared secret for the session,
        Use this secret to decrypt route and payload.

        Args:
            secret: Encrypted secret in base64 encoding.
            route: Encrypted route parameter in base64 encoding.
            payload: Encrypted request payload in base64 encoding.
        Return:
            Status: Success or Failure.
    """

    def _decrypt_helper(j_secret, j_payload):
        encryption_key = base64.b64decode(j_secret['key'])
        encryption_iv = base64.b64decode(j_secret['iv'])
        additional_data = base64.b64decode(j_secret['additionalData'])
        encryption_tag = base64.b64decode(j_payload['tag'])
        decrypter = Cipher(
            algorithms.AES(encryption_key),
            modes.GCM(encryption_iv, encryption_tag),
        ).decryptor()

        decrypter.authenticate_additional_data(additional_data)
        decrypted_msg = decrypter.update(base64.b64decode(j_payload['payload']))
        decrypter.finalize()
        return decrypted_msg

    secret_json = decrypt_secret(secret)
    decrypted_route = _decrypt_helper(secret_json, route).decode("utf-8")
    # Can validate route here before decrypting payload.
    decrypted_payload = json.loads(_decrypt_helper(secret_json, payload))
    return [decrypted_route, decrypted_payload]


def get_response_payload(secret, payload):
    """
        Given the shared secret for the session,
        Use this secret to encrypt the response.
        response payload will be a Json {payload: encrypted_payload, tag: encryption tag}
        If encryption fails return failure status with encryption failed reason.

        Args:
            secret: Encrypted secret in base64 encoding.
            payload: Response Json which is to be encrypted using secret.
        Return:
            Status: Success or Failure.
    """

    def _encrypt_helper(j_secret, j_payload):
        encryption_key = base64.b64decode(j_secret['key'])
        encryption_iv = base64.b64decode(j_secret['iv'])
        additional_data = base64.b64decode(j_secret['additionalData'])
        encryptor = Cipher(
            algorithms.AES(encryption_key),
            modes.GCM(encryption_iv),
        ).encryptor()
        encryptor.authenticate_additional_data(additional_data)
        payload_str = json.dumps(j_payload)
        ciphertext = encryptor.update(payload_str.encode('utf8'))
        encryptor.finalize()
        return_json = json.dumps({'payload': base64.b64encode(ciphertext).decode('ascii'),
                                  'tag': base64.b64encode(encryptor.tag).decode('ascii')})
        return return_json

    secret_json = decrypt_secret(secret)
    return _encrypt_helper(secret_json, payload)


@app.route('/rsa_pub', methods=["GET"])
def get_rsa_pub():
    """
        Returns: Returns a json with public RSA key.
    """
    public_rsa_key = app.config[constants.PUBLIC_RSA_KEY]
    response = {
        constants.STATUS: constants.STATUS_SUCCESS,
        constants.DATA: public_rsa_key
    }
    return jsonify(response)


@app.route('/', methods=['POST'])
def main():
    """
        This API is the only API used to communicate with frontend. From frontend, we will get encrypted payload
        and them we will use private key to decrypt the payload.
        Payload data contains route and post_data for post request.
    """
    main_json = json.loads(request.data)
    payload_json = json.loads(main_json['payload'])
    route_json = json.loads(main_json['route'])
    secret = main_json['secret']
    response = ""
    try:
        [route, request_json] = get_route_payload(secret, route_json, payload_json)
    except Exception as e:
        logging.error("Decryption error: " + str(e) + "\n" + traceback.format_exc())
        return jsonify({'status': 'failure', 'reason': 'Backend decryption failure'})

    if route == "/user_registration":
        response = user_registration(request_json)
    elif route == "/user_confirm_otp":
        response = user_confirm_otp(request_json)
    elif route == "/user_login":
        response = user_login(request_json)
    elif route == "/send_otp_without_token":
        response = user_send_otp_without_token(request_json)
    elif route == "/user_confirm_identity_otp":
        response = user_confirm_identity_otp(request_json)
    elif route == "/user_forgot_password":
        response = user_forgot_password(request_json)
    elif route == "/user_logout":
        response = user_logout()
    elif route == "/get_user_data":
        response = get_user_data(request_json)
    elif route == "/patient_info_update":
        response = patient_info_update(request_json)
    elif route == "/get_general_appointment_data":
        response = get_general_appointment_data()
    elif route == "/book_general_appointment":
        response = book_general_appointment(request_json)
    elif route == "/cancel_general_appointment":
        response = cancel_general_appointment(request_json)
    elif route == "/get_chatbot_reply":
        response = chatbot_reply(request_json)
    elif route == "/get_requested_appointments":
        response = get_requested_appointments()
    elif route == "/approve_appointment":
        response = approve_appointment(request_json)
    elif route == "/reject_appointment":
        response = reject_appointment(request_json)
    elif route == "/get_patient_from_email":
        response = get_patient_from_email(request_json)
    elif route == "/get_current_appointment_data":
        response = get_current_appointment_data(request_json)
    elif route == "/create_diagnosis_report":
        response = create_diagnosis_report(request_json)
    elif route == "/get_diagnosis_report":
        response = get_diagnosis_report(request_json)
    elif route == "/user_send_otp":
        response = user_send_otp(request_json)
    elif route == "/update_diagnosis_report":
        response = update_diagnosis_report(request_json)
    elif route == "/get_new_employee_account_request":
        response = get_new_employee_account_request()
    elif route == "/admin_approve_new_account":
        response = admin_approve_new_account(request_json)
    elif route == "/get_admin_logs":
        response = get_admin_logs_data()
    elif route == "/delete_user_record":
        response = delete_user_record(request_json)
    elif route == "/get_insurance_record":
        response = get_insurance_record(request_json)
    elif route == "/get_insurance_record_from_insurance_id":
        response = get_insurance_record_from_insurance_id(request_json)
    elif route == "/update_insurance_record":
        response = update_insurance_record(request_json)
    elif route == "/create_update_lab_report":
        response = create_update_lab_report(request_json)
    elif route == "/get_lab_records":
        response = get_lab_records()
    elif route == "/delete_lab_report":
        response = delete_lab_report(request_json)
    elif route == "/get_transactions_to_initiate":
        response = get_transactions_to_initiate()
    elif route == "/initiate_transaction":
        response = initiate_transaction(request_json)
    elif route == "/get_transactions_to_approve":
        response = get_transactions_to_approve()
    elif route == "/approve_reject_transactions":
        response = approve_reject_transactions(request_json)
    elif route == "/get_insurance_to_approve":
        response = get_insurance_to_approve()
    elif route == "/approve_reject_insurance_claim":
        response = approve_reject_insurance_claim(request_json)
    elif route == "/get_transactions":
        response = get_transactions(request_json)
    elif route == "/get_medical_records":
        response = get_medical_records(request_json)
    elif route == "/get_lab_record_by_appointment_id":
        response = get_lab_record_by_appointment_id(request_json)
    try:
        # second part is the response json
        response = get_response_payload(secret, response)
    except Exception as e:
        logging.error("Encryption error: " + str(e) + "\n" + traceback.format_exc())
        return jsonify({'status': 'failure', 'reason': 'Backend encryption failure'})

    return jsonify({'response': response})


# Auth APIs
def send_email(to_address, subject, message):
    """
        This method is used to send emails using SMTP protocol and Gmail server.

        Args:
            to_address: Email address of the recipient.
            subject: Subject of the Email.
            message: Body of the Email.
        Return:
            None
    """
    try:
        msg = Message(
            subject,
            sender=app.config[constants.EMAIL],
            recipients=[to_address]
        )
        msg.body = message
        mail.send(msg)
    except Exception as e:
        logging.error("Application send_email_api() Issue: \n" + str(e) + "\n" + traceback.format_exc())
        raise e


@app.route("/test")
def test():
    return "It is working."


def user_registration(post_data):
    """
        Registered user if not exist in the system and save the data in the DB.

        Return:
            Status: Success or Failure.
    """
    try:
        response = auth_api.user_registration_api(post_data)
        if response[constants.STATUS] == constants.STATUS_FAILURE:
            return response
        to_address = post_data[database_constants.USER_EMAIL]
        serializer = URLSafeTimedSerializer(app.config[constants.URL_GENERATOR_SECRET])
        token = serializer.dumps(to_address, salt=app.config[constants.EMAIL_SALT])
        link = url_for(endpoint='confirm_email', token=token, email=to_address, _external=True)
        subject = "Confirm Your Email Address"
        message = "Your Signup has been Successful. Please Click here " + link + " to confirm your email address."
        executor.submit(send_email, to_address=to_address, subject=subject, message=message)
        try:
            log_message = "User Registered, Email: " + post_data[database_constants.USER_EMAIL]
            executor.submit(admin_api.add_log_message, message=log_message)
        except Exception as err:
            logging.error("Application: Admin_log() issue: " + str(err) + "\n" + traceback.format_exc())
        return response
    except Exception as e:
        logging.error("Application: user_registration() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@app.route("/confirm_email/<token>/<email>")
def confirm_email(token, email):
    """
        This API is to confirm the email address of the user.

        Args:
            token: Encrypted time base token which was sent to user email address during registration process.
            email: Email address of the user that can be used to resend verification email if verification
            link is expired

        Return:
            Status: Verified or Not Verified HTML message
    """
    serializer = URLSafeTimedSerializer(app.config[constants.URL_GENERATOR_SECRET])
    try:
        email_address = serializer.loads(token, salt=app.config[constants.EMAIL_SALT], max_age=3600)
        mongo_client = mongo_db_api.get_database_client(constants.DATABASE_HMS)
        new_value = {"$set": {database_constants.USER_VERIFIED: True}}
        query = {database_constants.USER_HASH_EMAIL: cryptograpy_api.hash_encode(email_address)}
        mongo_db_api.update_one_into_db(mongo_client, constants.DATABASE_HMS,
                                        constants.COLLECTION_USERS, query, new_value)
        mongo_client.close()
        try:
            log_message = "User Verified, Email: " + email_address
            executor.submit(admin_api.add_log_message, message=log_message)
        except Exception as err:
            logging.error("Application: Admin_log() issue: " + str(err) + "\n" + traceback.format_exc())
        response = "<h1> Your email: " + email_address + " has been verified successfully.</h1>" \
                                                         "<a href='#login link'>Go to login page</a>"
        return response
    except SignatureExpired:
        try:
            token = serializer.dumps(email, salt=app.config[constants.EMAIL_SALT])
            link = url_for(endpoint="confirm_email", token=token, email=email, _external=True)
            subject = "From HMS: Confirm Your Email Address"
            message = "Your Signup has been Successful. Please Click here " + link + " to confirm your email address."
            executor.submit(send_email, to_address=email, subject=subject, message=message)
            return "<h1> The verification link is expired. A new Verification mail is been send to your mail " \
                   "address.</h1>"
        except Exception as e:
            subject = "Backend: confirm_email() Issue"
            message = str(e) + "\n" + traceback.format_exc() + "\n" + "Please check the logs."
            executor.submit(send_email, to_address=app.config[constants.EMAIL], subject=subject, message=message)
            logging.error("Application: confirm_email(), resend email issue: " + str(e) + "\n" + traceback.format_exc())
            return "<h1> Our Emails Server are down. Please try again later.</h1>"
    except Exception as e:
        logging.error("Application: confirm_email(), issue: " + str(e) + "\n" + traceback.format_exc())
        return "<h1> Our Emails Server are down. Please try again later.</h1>"


def user_login(post_data):
    """
        Logged-in user if it matches username and password.

        Return:
            Status: Success or Failure
    """
    try:
        response = auth_api.user_login_api(post_data)

        if response[constants.STATUS] == constants.STATUS_FAILURE:
            if response[constants.MESSAGE] == constants.MESSAGE_USER_NOT_VERIFIED:
                serializer = URLSafeTimedSerializer(app.config[constants.URL_GENERATOR_SECRET])
                to_address = post_data[database_constants.USER_EMAIL]
                token = serializer.dumps(to_address, salt=app.config[constants.EMAIL_SALT])
                link = url_for(endpoint='confirm_email', token=token, email=to_address, _external=True)
                subject = "Confirm Your Email Address."
                message = "Please Click here " + link + " to confirm your email address."
                executor.submit(send_email, to_address=to_address, subject=subject, message=message)
            return response

        otp = auth_api.generate_otp()
        to_address = post_data[database_constants.USER_EMAIL]
        subject = "HMS: Your One time Password to Login"
        message = "Hi. Here is the OTP to login to HMS: \"" + otp + "\".\nThis OTP is only valid for 10 minutes."
        executor.submit(send_email, to_address=to_address, subject=subject, message=message)
        redis_api.insert_into_redis(redis_client=redis, key=to_address, extended_key=constants.REDIS_OTP_EXTENDED_KEY,
                                    value=otp, expiry_timer=10)
        access_token = create_access_token(identity=to_address)
        response[constants.USER_API_ACCESS_TOKEN] = access_token
        try:
            log_message = "User Logged In, Email: " + post_data[database_constants.USER_EMAIL]
            executor.submit(admin_api.add_log_message, message=log_message)
        except Exception as err:
            logging.error("Application: Admin_log() issue: " + str(err) + "\n" + traceback.format_exc())
        return response
    except Exception as e:
        logging.error("Application: user_login() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def user_confirm_otp(post_data):
    """
        Verifying user entered otp.

        Return:
            Status: Success or Failure
    """
    try:
        email_address = get_jwt_identity()
        response = auth_api.user_confirm_otp_api(post_data=post_data, redis=redis, email_address=email_address)
        return response
    except Exception as e:
        logging.error("Application: user_confirm_otp() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def user_send_otp(post_data):
    """
        Verifying user entered otp after login step with jwt to authenticate user.

        Return:
            Status: Success or Failure
    """
    try:
        user_email = post_data[database_constants.USER_EMAIL]
        otp = auth_api.generate_otp()
        subject = "HMS: Your one time Password to confirm your identity!"
        message = "Hi, here is the OTP to confirm your identity: \"" + otp + \
                  "\".\nThis OTP is only valid for 10 minutes."
        executor.submit(send_email, to_address=user_email, subject=subject, message=message)
        redis_api.insert_into_redis(redis_client=redis, key=user_email, extended_key=constants.REDIS_OTP_EXTENDED_KEY,
                                    value=otp, expiry_timer=10)
        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.MESSAGE: constants.MESSAGE_OTP_SEND_SUCCESSFULLY
        }
        return response
    except Exception as e:
        logging.error("Application: user_send_otp() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


def user_send_otp_without_token(post_data):
    """
        Send otp to user who don't have token yet (not logged in)

        Return:
            Status: Success or Failure
    """
    try:
        if not auth_api.check_user_exists(post_data):
            response = {
                constants.STATUS: constants.STATUS_FAILURE,
                constants.MESSAGE: constants.MESSAGE_USER_NOT_EXIST
            }
            return response
        user_email = post_data[database_constants.USER_EMAIL]
        otp = auth_api.generate_otp()
        subject = "HMS: Your one time Password to confirm your identity!"
        message = "Hi, here is the OTP to confirm your identity: \"" + otp + \
                  "\".\nThis OTP is only valid for 10 minutes."
        executor.submit(send_email, to_address=user_email, subject=subject, message=message)
        redis_api.insert_into_redis(redis_client=redis, key=user_email, extended_key=constants.REDIS_OTP_EXTENDED_KEY,
                                    value=otp, expiry_timer=10)
        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.MESSAGE: constants.MESSAGE_OTP_SEND_SUCCESSFULLY
        }
        return response
    except Exception as e:
        print(str(e) + "\n" + traceback.format_exc())
        logging.error("Application: user_send_otp_without_token() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


def user_confirm_identity_otp(post_data):
    """
        Verifying user entered otp after verifying user who forgot their password.

        Return:
            Status: Success or Failure
    """
    try:
        response = auth_api.user_confirm_identity_otp_api(post_data=post_data, redis=redis)
        return response
    except Exception as e:
        logging.error("Application: user_confirm_identity_otp() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


def user_forgot_password(post_data):
    """
        Updating user password with new password after verifying user.

        Return:
            Status: Success or Failure
    """
    try:
        response = auth_api.user_forgot_password_api(post_data=post_data)
        return response
    except Exception as e:
        logging.error("Application: user_forgot_password() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def user_logout():
    """
        Logging out user. Revoking token access to prevent unauthorized access.

        Return:
            Status: Success or Failure
    """
    try:
        json_token_identifier = get_jwt()[constants.JSON_TOKEN_IDENTIFIER]
        redis.set(json_token_identifier, "", ex=timedelta(minutes=constants.JWT_ACCESS_TOKEN_EXPIRES_TIME_MINUTES))
        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.MESSAGE: constants.MESSAGE_ACCESS_REVOKED
        }
        try:
            log_message = "User Logged out, Token Identifier: " + str(json_token_identifier)
            executor.submit(admin_api.add_log_message, message=log_message)
        except Exception as err:
            logging.error("Application: Admin_log() issue: " + str(err) + "\n" + traceback.format_exc())
        return response
    except Exception as e:
        logging.error("Application: user_logout() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE
# Auth APIs Completed


# Common User API
@jwt_required()
def get_user_data(user_data):
    try:
        response = patient_api.get_user_data(user_data)
        try:
            log_message = "User Getting data, Email: " + user_data[database_constants.USER_EMAIL]
            executor.submit(admin_api.add_log_message, message=log_message)
        except Exception as err:
            logging.error("Application: Admin_log() issue: " + str(err) + "\n" + traceback.format_exc())
        return response
    except Exception as e:
        logging.error("Application: get_user_data() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


# Patient APIs
@jwt_required()
def patient_info_update(post_data):
    """
        This API updates the user information

        Returns: None
    """
    try:
        response = patient_api.update_patient_info(post_data)
        try:
            log_message = "User Information Updated: " + post_data[database_constants.USER_EMAIL]
            executor.submit(admin_api.add_log_message, message=log_message)
        except Exception as err:
            logging.error("Application: Admin_log() issue: " + str(err) + "\n" + traceback.format_exc())
        return response
    except Exception as e:
        logging.error("Application: patient_info_update() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def get_general_appointment_data():
    """
        This API updates the user information

        Returns: Array of available appointment slot
    """
    try:
        return patient_api.get_appointment_data()
    except Exception as e:
        logging.error("Application: get_general_appointment_data() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def book_general_appointment(post_data):
    """
        This API books appointment

        Returns: Status of the operation
    """
    try:
        response = patient_api.book_general_appointment(post_data)
        try:
            log_message = "User Booked Appointment: " + post_data[database_constants.APPOINTMENT_USER_EMAIL]
            executor.submit(admin_api.add_log_message, message=log_message)
        except Exception as err:
            logging.error("Application: Admin_log() issue: " + str(err) + "\n" + traceback.format_exc())
        return response
    except Exception as e:
        logging.error("Application: book_general_appointment() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def cancel_general_appointment(post_data):
    """
        This API cancels appointment

        Returns: Status of the operation
    """
    try:
        response = patient_api.cancel_general_appointment(post_data)
        try:
            log_message = "User Cancelled Appointment, Email: " + post_data[database_constants.USER_EMAIL]
            executor.submit(admin_api.add_log_message, message=log_message)
        except Exception as err:
            logging.error("Application: Admin_log() issue: " + str(err) + "\n" + traceback.format_exc())
        return response
    except Exception as e:
        logging.error("Application: book_general_appointment() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def get_medical_records(post_data):
    """
        This API cancels appointment

        Returns: Status of the operation
    """
    try:
        response = patient_api.get_medical_records(post_data)
        try:
            log_message = "User Get Medial Records, User Id: " + post_data[database_constants.USER_USER_ID]
            executor.submit(admin_api.add_log_message, message=log_message)
        except Exception as err:
            logging.error("Application: Admin_log() issue: " + str(err) + "\n" + traceback.format_exc())
        return response
    except Exception as e:
        logging.error("Application: get_medical_records() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def get_transactions(post_data):
    try:
        response = patient_api.get_transactions(post_data)
        return response
    except Exception as e:
        logging.error("Application: get_transactions() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE
# Patient APIs Completed


# Doctor API
@jwt_required()
def get_current_appointment_data(post_data):
    try:
        response = doctor_api.get_current_appointment_details(post_data)
        return response
    except Exception as e:
        logging.error("Application: get_current_appointment_data() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def create_diagnosis_report(post_data):
    try:
        # post_data = request.json
        response = doctor_api.create_diagnosis_report(post_data)
        try:
            log_message = "Doctor: Created Diagnosis Report: Doctor ID: " + \
                          post_data[database_constants.DIAGNOSIS_DOCTOR_ID] + " User email: " + \
                          post_data[database_constants.DIAGNOSIS_USER_EMAIL]
            executor.submit(admin_api.add_log_message, message=log_message)
        except Exception as err:
            logging.error("Application: Admin_log() issue: " + str(err) + "\n" + traceback.format_exc())
        return response
    except Exception as e:
        logging.error("Application: create_diagnosis_report() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def get_diagnosis_report(post_data):
    try:
        response = doctor_api.get_diagnosis_report(post_data)
        return response
    except Exception as e:
        logging.error("Application: get_diagnosis_report() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def update_diagnosis_report(post_data):
    try:
        response = doctor_api.update_diagnosis_report(post_data)
        return response
    except Exception as e:
        logging.error("Application: update_diagnosis_report() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE
# Doctor API completed


# Insurance API
@jwt_required()
def get_insurance_record(user_data):
    try:
        response = insurance_api.get_insurance_record(user_data)
        return response
    except Exception as e:
        logging.error("Application: get_insurance_details() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def get_insurance_record_from_insurance_id(user_data):
    try:
        response = insurance_api.get_insurance_record_from_insurance_id(user_data)
        return response
    except Exception as e:
        logging.error(
            "Application: get_insurance_record_from_insurance_id() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def get_insurance_record_from_insurance_id(user_data):
    try:
        response = insurance_api.get_insurance_record_from_insurance_id(user_data)
        return response
    except Exception as e:
        logging.error(
            "Application: get_insurance_record_from_insurance_id() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def update_insurance_record(user_data):
    try:
        response = insurance_api.update_insurance_record(user_data)
        return response
    except Exception as e:
        logging.error("Application: create_insurance_to_patients() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def get_insurance_to_approve():
    try:
        response = insurance_api.get_insurance_to_approve()
        return {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.DATA: response,
        }
    except Exception as e:
        logging.error("Application: get_insurance_to_approve() issue: " + str(e) + "\n" + traceback.format_exc())
        return {
            constants.STATUS: constants.STATUS_FAILURE,
            constants.MESSAGE: constants.MESSAGE_NO_TRANSACTION_TO_APPROVE
        }


@jwt_required()
def approve_reject_insurance_claim(post_data):
    try:
        response = insurance_api.approve_reject_transactions(post_data)
        return response
    except Exception as e:
        logging.error("Application: approve_reject_insurance_claim() issue: " + str(e) + "\n" + traceback.format_exc())
        return {
            constants.STATUS: constants.STATUS_FAILURE,
            constants.MESSAGE: constants.MESSAGE_FAILED_CHANGE_TRANSACTION_STATUS
        }


# Appointment URLs
@jwt_required()
def get_requested_appointments():
    try:
        reply = hospital_staff_api.get_requested_appointments()
        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.DATA: reply,
            constants.MESSAGE: constants.STATUS_SUCCESS
        }
    except Exception as e:
        logging.error("Application: Issue getting appointments. issue: " + str(e) + "\n" + traceback.format_exc())
        response = {
            constants.STATUS: constants.STATUS_FAILURE,
            constants.MESSAGE: constants.MESSAGE_ERROR_APPOINTMENT
        }
    return response


@jwt_required()
def approve_appointment(post_data):
    """
        This API books appointment

        Returns: Status of the operation
    """
    try:
        response = hospital_staff_api.approve_reject_appointment(post_data)
        try:
            log_message = "Hospital Staff: Approved Appointment, User Email: " + \
                          post_data[database_constants.APPOINTMENT_USER_EMAIL]
            executor.submit(admin_api.add_log_message, message=log_message)
        except Exception as err:
            logging.error("Application: Admin_log() issue: " + str(err) + "\n" + traceback.format_exc())
        if response[constants.STATUS] == constants.STATUS_SUCCESS:
            appointment_id = post_data[database_constants.APPOINTMENT_APPOINTMENT_ID]
            subject = "Appointment confirmed"
            message = "Your appointment with {} at {} is confirmed and your appointment id " \
                      "is:{}".format(post_data["doctor_name"], post_data[database_constants.APPOINTMENT_TIME],
                                     appointment_id)
            executor.submit(send_email, to_address=post_data[database_constants.APPOINTMENT_USER_EMAIL],
                            subject=subject, message=message)
        return response
    except Exception as e:
        logging.error("Application: approve_appointment() issue: " + str(e) + "\n" + traceback.format_exc())
        return {constants.STATUS: constants.RESPONSE_FAILURE}


@jwt_required()
def reject_appointment(post_data):
    """
        This API books appointment

        Returns: Status of the operation
    """
    try:
        response = hospital_staff_api.approve_reject_appointment(post_data, False)

        try:
            log_message = "Hospital Staff: Rejected Appointment, User Email: " + \
                          post_data[database_constants.APPOINTMENT_USER_EMAIL]
            executor.submit(admin_api.add_log_message, message=log_message)
        except Exception as err:
            logging.error("Application: Admin_log() issue: " + str(err) + "\n" + traceback.format_exc())

        if response[constants.STATUS] == constants.STATUS_SUCCESS:
            subject = "Appointment not approved"
            message = "Your appointment with {} at {} is not approved".format(post_data["doctor_name"],
                                                                              post_data[database_constants.
                                                                              APPOINTMENT_TIME])
            executor.submit(send_email, to_address=post_data[database_constants.APPOINTMENT_USER_EMAIL],
                            subject=subject, message=message)
        return response
    except Exception as e:
        logging.error("Application: reject_appointment() issue: " + str(e) + "\n" + traceback.format_exc())
        return {constants.STATUS: constants.RESPONSE_FAILURE}


@jwt_required()
def get_transactions_to_initiate():
    try:
        data = hospital_staff_api.get_transactions_to_initiate()
        msg = constants.STATUS_SUCCESS
        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.DATA: data,
            constants.MESSAGE: msg
        }
    except Exception as e:
        logging.error("Application: get_transactions_to_initiate() " + str(e) + "\n" + traceback.format_exc())
        response = {
            constants.STATUS: constants.STATUS_FAILURE,
            constants.MESSAGE_NO_NEW_TRANSACTION_AVAILABLE: constants.MESSAGE_NO_NEW_TRANSACTION_AVAILABLE
        }
    return response


@jwt_required()
def initiate_transaction(post_data):
    try:
        hospital_staff_api.initiate_transaction(post_data)
        return {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.MESSAGE: constants.MESSAGE_INITIATED_SUCCESSFULLY
        }
    except Exception as e:
        logging.error("Application: initiate_transaction() " + str(e) + "\n" + traceback.format_exc())
        return {
            constants.STATUS: constants.STATUS_FAILURE,
            constants.MESSAGE: constants.MESSAGE_INITIATED_FAILED
        }


@jwt_required()
def get_patient_from_email(post_data):
    try:
        data = patient_api.get_user_details(post_data)
        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.DATA: data,
            constants.MESSAGE: constants.STATUS_SUCCESS
        }
    except Exception as e:
        logging.error("Application: get_patient_from_email() " + str(e) + "\n" + traceback.format_exc())
        response = {
            constants.STATUS: constants.STATUS_FAILURE,
            constants.MESSAGE: constants.MESSAGE_ERROR_GETTING_USER_DATA
        }
    return response
# Insurance APIs Completed


# chatbot API
@jwt_required()
def chatbot_reply(chat_context):
    try:
        reply = my_chat_bot.get_chatbot_reply(chat_context[database_constants.USER_USER_TYPE], chat_context[
            database_constants.CHAT_QUERY])
        response = {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.DATA: reply,
            constants.MESSAGE: constants.MESSAGE_CHATBOT_SUCCESS
        }
    except Exception as e:
        logging.error("Application: chatbot_reply() issue: " + str(e) + "\n" + traceback.format_exc())
        response = {
            constants.STATUS: constants.STATUS_FAILURE,
            constants.MESSAGE: constants.MESSAGE_CHATBOT_FAILURE
        }
    return response
# chatbot API completed


# Admin API
@jwt_required()
def get_new_employee_account_request():
    try:
        response = admin_api.get_new_created_account()
        try:
            log_message = "Get_new_employee_account_request"
            executor.submit(admin_api.add_log_message, message=log_message)
        except Exception as err:
            logging.error("Application: Admin_log() issue: " + str(err) + "\n" + traceback.format_exc())
        return response
    except Exception as e:
        logging.error("Application: approve_new_employee_account() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def admin_approve_new_account(post_data):
    try:
        response = admin_api.approve_new_account(post_data)
        try:
            log_message = "Admin Approved, Rejected Account, User ID: " + post_data[database_constants.USER_USER_ID]
            executor.submit(admin_api.add_log_message, message=log_message)
        except Exception as err:
            logging.error("Application: Admin_log() issue: " + str(err) + "\n" + traceback.format_exc())
        return response
    except Exception as e:
        logging.error("Application: admin_approve_new_account() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def get_admin_logs_data():
    try:
        response = admin_api.get_admin_logs()
        return response
    except Exception as e:
        logging.error("Application: get_admin_logs_data() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def delete_user_record(post_data):
    try:
        response = admin_api.delete_user_record(post_data)
        return response
    except Exception as e:
        logging.error("Application: delete_user_record() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def get_transactions_to_approve():
    try:
        response = admin_api.get_transactions_to_approve()
        return {
            constants.STATUS: constants.STATUS_SUCCESS,
            constants.DATA: response,
        }
    except Exception as e:
        logging.error("Application: get_transactions_to_approve() issue: " + str(e) + "\n" + traceback.format_exc())
        return {
            constants.STATUS: constants.STATUS_FAILURE,
            constants.MESSAGE: constants.MESSAGE_NO_TRANSACTION_TO_APPROVE
        }


@jwt_required()
def approve_reject_transactions(post_data):
    try:
        response = admin_api.approve_reject_transactions(post_data)
        data = response[constants.DATA]
        executor.submit(post_transaction_to_block_chain, record=data)
        try:
            log_message = "Approve_reject_transactions, Transaction ID: " + post_data[database_constants.TRANSACTION_ID]
            executor.submit(admin_api.add_log_message, message=log_message)
        except Exception as err:
            logging.error("Application: Admin_log() issue: " + str(err) + "\n" + traceback.format_exc())
        return response
    except Exception as e:
        logging.error(e)
        return {
            constants.STATUS: constants.STATUS_FAILURE,
            constants.MESSAGE: constants.MESSAGE_FAILED_CHANGE_TRANSACTION_STATUS
        }
# Admin API completed


# LAB STAFF API
@jwt_required()
def get_lab_records():
    try:
        response = lab_api.get_requested_lab_test()
        return response
    except Exception as e:
        logging.error("Application: get_lab_records() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def get_lab_record_by_appointment_id(post_data):
    try:
        response = lab_api.get_lab_record_by_appointment_id(post_data)
        try:
            log_message = "get_lab_record_by_appointment_id(), Appointment ID: " + \
                          post_data[database_constants.LAB_APPOINTMENT_ID]
            executor.submit(admin_api.add_log_message, message=log_message)
        except Exception as err:
            logging.error("Application: Admin_log() issue: " + str(err) + "\n" + traceback.format_exc())
        return response
    except Exception as e:
        logging.error("Application: get_lab_record_by_appointment_id() issue: " + str(e) + "\n" +
                      traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def create_update_lab_report(post_data):
    try:
        response = lab_api.create_update_lab_report(post_data)
        try:
            log_message = "Create_update_lab_report, Appointment ID: " + \
                          post_data[database_constants.LAB_APPOINTMENT_ID]
            executor.submit(admin_api.add_log_message, message=log_message)
        except Exception as err:
            logging.error("Application: Admin_log() issue: " + str(err) + "\n" + traceback.format_exc())
        return response
    except Exception as e:
        logging.error("Application: create_update_lab_report() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE


@jwt_required()
def delete_lab_report(post_data):
    try:
        response = lab_api.delete_lab_report(post_data)
        try:
            log_message = "Delete Lab Record, Email: " + post_data[database_constants.LAB_ID]
            executor.submit(admin_api.add_log_message, message=log_message)
        except Exception as err:
            logging.error("Application: Admin_log() issue: " + str(err) + "\n" + traceback.format_exc())
        return response
    except Exception as e:
        logging.error("Application: delete_lab_report() issue: " + str(e) + "\n" + traceback.format_exc())
        return constants.RESPONSE_FAILURE
# LAB STAFF API


# BLOCKCHAIN API
def post_transaction_to_block_chain(record):
    url = app.config[constants.BLOCKCHAIN_URL]
    requests.post(url=url, json=record)
# BLOCKCHAIN API


# We will use gunicorn in production, so setting logger for gunicorn as gunicorn use multiprocessing.
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

# Set debug to false while in production
if __name__ == "__main__":
    logger = backend_logger.get_logger(__name__)
    logging.info('=========================Backend Started=========================')
    app.run(host="0.0.0.0", port=8000, debug=True)
