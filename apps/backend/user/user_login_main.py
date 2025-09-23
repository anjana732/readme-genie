import json
import secrets
from datetime import datetime, timedelta

from config import SCHEMA, USER_TABLE, OTP_TABLE
from utils import *


class UserMobileLogin:
    def __init__(self, data):
        self.data = data
        self.mobile = data.get("mobile")
        self.otp = self.data.get("otp", None)
        self.user_id = self.data.get("user_id", None)

    def check_existing_user(self):
        func_status = True
        is_existing_user = True
        try:
            qry = """SELECT * FROM {0}.{1} where mobile_number = %s and is_mobile_verified = 1 order by 1 desc limit 1""".format(SCHEMA, USER_TABLE)
            params = (self.mobile,)
            qry_status, user_df = get_data_from_db(qry, SCHEMA, params)
            if not qry_status:
                raise Exception("Error in fetching user data from DB")

            if user_df.empty:
                is_existing_user = False

            self.user_id = user_df['user_id'].values[0] if is_existing_user else None

        except Exception as e:
            handle_exception("check_existing_user", sys.exc_info(), e)
            func_status = False
            is_existing_user = False

        return func_status, is_existing_user

    def otp_generate(self):
        func_status = True
        try:
            # OTP GENERATION LOGIC
            self.otp = ''.join(secrets.choice("0123456789") for _ in range(6))  # Placeholder for actual OTP generation logic

        except Exception as e:
            handle_exception("otp_generate", sys.exc_info(), e)
            func_status = False

        return func_status

    def otp_sent_api(self):
        func_status = True
        api_status = True
        try:
            # API CALL TO SEND OTP
            response_text = '''
            {
                "return": true,
                "request_id": "lwdtp7cjyqxvfe9",
                "message": [
                    "Message sent successfully"
                ]
            }
            '''

            response = json.loads(response_text)
            print(response)
            if response.get("return") not in (True, 'true'):
                api_status = False

        except Exception as e:
            handle_exception("otp_sent_api", sys.exc_info(), e)
            func_status = False
            api_status = False

        return func_status, api_status

    def send_otp_to_mobile(self):

        func_status = True
        otp_sent_status = True
        try:
            otp_api_func_status, api_status = self.otp_sent_api()
            if not otp_api_func_status or not api_status:
                raise Exception("Error in sending OTP to mobile")

        except Exception as e:
            handle_exception("send_otp_to_mobile", sys.exc_info(), e)
            func_status = False
            otp_sent_status = False

        return func_status, otp_sent_status

    def store_otp_in_db(self):
        func_status = True
        try:
            expires_at = datetime.now() + timedelta(minutes=10)
            qry = f"""
            INSERT INTO {SCHEMA}.{OTP_TABLE}
            (user_id, otp, mobile_number, expires_at, is_used)
            VALUES (:user_id, :otp, :mobile, :expires_at, :is_used);
            """
            params = {
                "user_id": self.user_id,
                "otp": self.otp,
                "mobile": self.mobile,
                "expires_at": expires_at,
                "is_used": 0
            }
            qry_status, _ = insert_data_to_db(qry, SCHEMA, params)
            if not qry_status:
                raise Exception("Error in storing OTP in DB")

        except Exception as e:
            handle_exception("store_otp_in_db", sys.exc_info(), e)
            func_status = False

        return func_status

    def user_login_main_func(self):
        func_status = True
        is_success = False
        message = None
        is_existing_user = False
        is_otp_sent = False
        try:
            func_status, is_existing_user = self.check_existing_user()
            if not func_status:
                raise Exception("Error in checking existing user")

            if not is_existing_user:
                message = "User does not exist. Please sign up."
                return func_status, is_existing_user, is_otp_sent, message

            # Generate and send OTP
            otp_generate_func_status = self.otp_generate()
            if not otp_generate_func_status:
                raise Exception("Error in generating OTP, Please try again !!")

            func_status, is_otp_sent = self.send_otp_to_mobile()
            if (
                    not func_status or
                    not is_otp_sent
            ):
                raise Exception("Failed to send OTP, Please try again !!")

            store_otp_func_status = self.store_otp_in_db()
            if not store_otp_func_status:
                raise Exception("Error in storing OTP, Please try again !!")

            message = "OTP verification sent to your mobile number."


        except Exception as e:
            handle_exception("user_login_main_func", sys.exc_info(), e)
            func_status = False
            message = e

        return func_status, is_existing_user, is_otp_sent, message

    def check_otp(self):
        func_status = True
        is_otp_verified = False
        try:
            qry = """SELECT * FROM {0}.{1} where user_id = %s and otp = %s and is_used = 0 and expires_at > NOW() order by 1 desc limit 1""".format(SCHEMA, OTP_TABLE)
            params = (self.user_id, self.otp,)
            qry_status, otp_df = get_data_from_db(qry, SCHEMA, params)

            if not qry_status:
                raise Exception("Error in fetching OTP data from DB")

            if otp_df.empty:
                return func_status, is_otp_verified

            # Mark OTP as used
            otp_id = otp_df['otp_id'].values[0]
            update_qry = f"UPDATE {SCHEMA}.{OTP_TABLE} SET is_used = 1 WHERE otp_id = :otp_id"
            update_params = {"otp_id": otp_id}
            update_status, _ = insert_data_to_db(update_qry, SCHEMA, update_params)
            if not update_status:
                raise Exception("Error in updating OTP status in DB")

            is_otp_verified = True

        except Exception as e:
            handle_exception("check_otp", sys.exc_info(), e)
            func_status = False

        return func_status, is_otp_verified

    def verify_otp(self):
        is_otp_verified = False
        func_status = True
        message = None
        try:
            func_status, is_otp_verified = self.check_otp()
            if not func_status:
                raise Exception("OTP verification failed, Please try again !!")

            if not is_otp_verified:
                raise Exception("Invalid OTP, Please try again !!")

            message = "OTP verified successfully."

        except Exception as e:
            handle_exception("verify_otp", sys.exc_info(), e)
            func_status = False
            message = str(e)

        return func_status, is_otp_verified, message
