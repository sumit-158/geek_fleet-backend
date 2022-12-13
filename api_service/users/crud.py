from utils.dbUtil import database
from utils import cryptoUtil
from users import schemas as user_schema
from auth import schemas as auth_schema
from models import logOutlists


def update_user(request: user_schema.UpdateUser, currentUser: auth_schema.UserList):
    query = "UPDATE my_users SET fullname=:fullname, state=:state, city=:city, email=:email where phone_number=:phone_number"
    return database.execute(
        query,
        values={
            "fullname": currentUser.fullname
            if request.fullname is None
            else request.fullname,
            "state": currentUser.state if request.state is None else request.state,
            "city": currentUser.city if request.city is None else request.city,
            "email": currentUser.email if request.email is None else request.email,
            "phone_number": currentUser.phone_number,
        },
    )


def deactivate_user(currentUser: auth_schema.UserList):
    query = (
        "UPDATE my_users SET status='9' where status='1' and phone_number=:phone_number"
    )
    return database.execute(query, values={"phone_number": currentUser.phone_number})


def change_password(
    chgPwd: auth_schema.ChangePassword, currentUser: auth_schema.UserList
):
    query = "UPDATE my_users SET password=:password WHERE phone_number=:phone_number"
    return database.execute(
        query=query,
        values={
            "password": cryptoUtil.get_password_hash(chgPwd.new_password),
            "phone_number": currentUser.phone_number,
        },
    )


def set_logout_list(token: str, currentUser: auth_schema.UserList):
    query = logOutlists.insert().values(
        token=token,
        phone_number=currentUser.phone_number,
    )
    return database.execute(query)
