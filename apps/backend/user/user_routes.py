from fastapi import APIRouter
from pydantic import BaseModel
from user.user_login_main import UserLogin


class UserLoginModel(BaseModel):
    username: str
    password: str


user_router = APIRouter(
    prefix="/login",
    tags=["user operations"]
)


@user_router.post("/")
def user_login(body: UserLoginModel):
    func_status = True
    is_success = False
    message = None
    try:
        user_login_obj = UserLogin(body)
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
