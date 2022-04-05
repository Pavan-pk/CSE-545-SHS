# USER TABLE
USER_USER_ID = "user_id"
USER_FULL_NAME = "full_name"
USER_BIRTH_DATE = "birth_date"
USER_EMAIL = "email"
USER_HASH_EMAIL = "hash_email"
USER_PASSWORD = "password"
USER_USER_TYPE = "user_type"
USER_VERIFIED = "verified"
USER_GENDER = "gender"
USER_CONTACT_NUMBER = "contact_number"
USER_SPECIALITY = "user_speciality"
USER_INSURANCE_ID = "user_insurance"
USER_APPROVED = "approved"


# INSURANCE TABLE
INSURANCE_ID = "insurance_id"
INSURANCE_USER_ID = "user_id"
INSURANCE_FULL_NAME = "full_name"
INSURANCE_USER_EMAIL = "email"
INSURANCE_USER_HASH_EMAIL = "hash_email"
INSURANCE_RENEW_DATE = "renew_date"
INSURANCE_VALIDITY_DATE = "validity_date"


# APPOINTMENT TABLE
APPOINTMENT_APPOINTMENT_ID = "appointment_id"
APPOINTMENT_DATE = "date"
APPOINTMENT_TIME = "time"
APPOINTMENT_USER_ID = "user_id"
APPOINTMENT_USER_EMAIL = "user_email"
APPOINTMENT_STATUS = "status"
APPOINTMENT_DOCTOR_ID = "doctor_id"
APPOINTMENT_DOCTOR_NAME = "doctor_name"
APPOINTMENT_DOCTOR_EMAIL = "doctor_email"
APPOINTMENT_DOCTOR_SPECIALITY = "doctor_speciality"


# DIAGNOSIS TABLE
DIAGNOSIS_ID = "diagnosis_id"
DIAGNOSIS_PRESCRIPTION_ID = "prescription_id"
DIAGNOSIS_LAB_ID = "lab_id"
DIAGNOSIS_USER_ID = "user_id"
DIAGNOSIS_USER_EMAIL = "user_email"
DIAGNOSIS_DOCTOR_ID = "doctor_id"
DIAGNOSIS_DOCTOR_NAME = "doctor_name"
DIAGNOSIS_DOCTOR_EMAIL = "doctor_email"
DIAGNOSIS_RECORD = "diagnosis_record"
DIAGNOSIS_APPOINTMENT_ID = "appointment_id"
DIAGNOSIS_DATE = "date"
DIAGNOSIS_TIME = "time"
DIAGNOSIS_STATUS = "status"


# LAB TABLE
LAB_ID = "lab_id"
LAB_USER_ID = "user_id"
LAB_DOCTOR_ID = "doctor_id"
LAB_DIAGNOSIS_ID = "diagnosis_id"
LAB_USER_EMAIL = "user_email"
LAB_DOCTOR_EMAIL = "doctor_email"
LAB_APPOINTMENT_ID = "appointment_id"
LAB_TEST = "lab_recommendation"
LAB_REPORT = "lab_report"
LAB_DATE = "date"
LAB_TIME = "time"
LAB_STATUS = "status"


# PRESCRIPTION TABLE
PRESCRIPTION_ID = "prescription_id"
PRESCRIPTION_USER_ID = "user_id"
PRESCRIPTION_DOCTOR_ID = "doctor_id"
PRESCRIPTION_DIAGNOSIS_ID = "diagnosis_id"
PRESCRIPTION_USER_EMAIL = "user_email"
PRESCRIPTION_DOCTOR_EMAIL = "doctor_email"
PRESCRIPTION_APPOINTMENT_ID = "appointment_id"
PRESCRIPTION_RECORD = "prescription_record"
PRESCRIPTION_DATE = "date"
PRESCRIPTION_TIME = "time"
PRESCRIPTION_STATUS = "status"


# ADMIN_LOG TABLE
ADMIN_LOG_ID = "log_record_id"
ADMIN_LOG_DATE = "date"
ADMIN_LOG_TIME = "time"
ADMIN_LOG_MESSAGE = "message"


# TRANSACTION TABLE
TRANSACTION_ID = "transaction_id"
TRANSACTION_APPOINTMENT_ID = "appointment_id"
TRANSACTION_USER_ID = "user_id"
TRANSACTION_USER_TYPE = "user_type"
TRANSACTION_USER_EMAIL = "email"
TRANSACTION_USER_BIRTH_DATE = "birth_date"
TRANSACTION_TYPE = "transaction_type"
TRANSACTION_DETAILS = "transaction_details"
TRANSACTION_REASON = "reason"
TRANSACTION_AMOUNT = "transaction_amount"
TRANSACTION_STATUS = "status"

# FRONT END CONSTANT
FRONT_END_USER_EMAIL = "user_email"


# MISC
CHAT_QUERY = "query"

