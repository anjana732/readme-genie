import copy
import re

from fastapi import APIRouter
from pydantic import BaseModel, field_validator

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


@user_router.post("/phone")
def user_login(body: MobileLoginModel):
    func_status = True
    data = copy.deepcopy(body.model_dump())
    is_success = False
    message = None
    try:
        user_login_obj = UserMobileLogin(data)
        func_status, is_success, message = user_login_obj.user_login_main_func()
        if not func_status:
            raise Exception("Error in user login, Please try again !!")

    except Exception as e:
        func_status = False
        message = str(e)

    return {
        "is_successful_login": is_success,
        "message": message
    }
