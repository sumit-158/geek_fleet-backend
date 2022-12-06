from api.utils.dbUtil import database
from api.auth import schemas


def save_user(user: schemas.UserCreate):
    query = "INSERT INTO my_users VALUES (nextval('user_id_seq'), :email, :password, :fullname, :phone_number, :state, :city, now() at time zone 'UTC', '1')"
    return database.execute(
        query,
        values={
            "email": user.email,
            "password": user.password,
            "fullname": user.fullname,
            "phone_number": user.phone_number,
            "state": user.state,
            "city": user.city,
        },
    )


def find_existed_user(phone_number: int):
    query = "select * from my_users where phone_number=:phone_number and status='1'"
    return database.fetch_one(query, values={"phone_number": phone_number})


def reset_password(new_password: str, phone_number: int):
    query = "UPDATE my_users SET password=:password WHERE phone_number=:phone_number"
    return database.execute(
        query=query, values={"password": new_password, "phone_number": phone_number}
    )


def find_token_logout_lists(token: str):
    query = "select * from my_logoutlists where token=:token"
    return database.fetch_one(query, values={"token": token})
