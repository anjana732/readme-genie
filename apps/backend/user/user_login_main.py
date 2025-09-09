import re


class UserLogin:
    def __init__(self, body):
        self.body = body
        self.user_name = body.username
        self.password = body.password

    def is_mobile_number(self):
        """
        Check if the given string is a valid Indian mobile number.
        """
        func_status = True
        match_status = False
        try:
            pattern = r"^[6-9]\d{9}$"
            match_status = bool(re.match(pattern, self.user_name))

        except Exception as e:
            print(e)
            func_status = False

        return func_status, match_status

    def user_mobile_login(self):
        func_status = True
        is_sucuess = True
        message = "Mobile Login Successful"
        return func_status, is_sucuess, message

    def is_email(self):
        return True, ""

    def user_email_login(self):
        func_status = True
        is_success = False
        message = None
        return func_status, is_success, message

    def user_login_main_func(self):
        func_status = True
        is_success = False
        try:
            check_mobile_func_status, mobile_match_status = self.is_mobile_number()

            if not check_mobile_func_status:
                raise Exception("Error in validating the mobile number")

            if mobile_match_status:
                mobile_match_func_status, is_success, message = self.user_mobile_login()

                if not mobile_match_func_status:
                    raise Exception("Error in validating the mobile number")

                return func_status, is_success, message

            check_email_func_status, mobile_match_status = self.is_email()
            if not check_email_func_status:
                raise Exception("Error in validating the email")

            func_status, is_success, message = self.user_email_login()

        except Exception as e:
            message = e
            func_status = False

        return func_status, is_success, message
