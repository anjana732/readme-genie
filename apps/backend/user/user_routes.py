import copy
import re
import sys

from fastapi import APIRouter, Body
from pydantic import BaseModel, field_validator

from handle_exception import handle_exception
from user.user_login_main import UserMobileLogin


class MobileLoginModel(BaseModel):
    mobile: str

    @field_validator("mobile")
    def validate_mobile(cls, v: str) -> str:
        if not re.fullmatch(r"^[6-9]\d{9}$", v):
            raise ValueError("Invalid mobile number format")
        return v


user_router = APIRouter(
    prefix="/auth",
    tags=["user operations"]
)


class OTPVerifyModel(BaseModel):
    user_id: int
    otp: str

    @field_validator("otp")
    def validate_otp(cls, v: str) -> str:
        if not re.fullmatch(r"^\d{6}$", v):
            raise ValueError("Invalid OTP format")
        return v


@user_router.post("/phone")
def user_login(body: MobileLoginModel):
    func_status = True
    data = copy.deepcopy(body.model_dump())
    is_existing_user = False
    is_otp_sent = False
    message = None
    try:
        user_login_obj = UserMobileLogin(data)
        func_status, is_existing_user, is_otp_sent, message = user_login_obj.user_login_main_func()
        if not func_status:
            raise Exception("Error in user login, Please try again !!")

    except Exception as e:
        handle_exception("user_login", sys.exc_info(), e)
        func_status = False
        message = str(e)

    return {
        "is_otp_sent": is_otp_sent,
        "message": message,
        "is_existing_user": is_existing_user,

    }


@user_router.post("/phone/verify")
def verify_otp(body: OTPVerifyModel = Body(...)):
    is_otp_verified = False
    message = None
    try:
        data = copy.deepcopy(body.model_dump())
        user_login_obj = UserMobileLogin(data)
        func_status, is_otp_verified, message = user_login_obj.verify_otp()

        if not func_status:
            raise Exception("Error in verifying the OTP, Please try again !!")

        message = "OTP verified successfully." if is_otp_verified else "Invalid OTP, Please try again !!"

    except Exception as e:
        handle_exception("verify_otp", sys.exc_info(), e)
        message = str(e)

    return {
        "is_otp_verified": is_otp_verified,
        "message": message
    }
