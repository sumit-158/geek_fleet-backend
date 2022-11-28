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


def create_reset_code(request: schemas.PhoneRequest, reset_code: int):
    query = "INSERT INTO my_codes VALUES (nextval('code_id_seq'), :phone_number, :reset_code, '1', now() at time zone 'UTC')"
    return database.execute(
        query, values={"phone_number": request.phone_number, "reset_code": reset_code}
    )


def check_reset_password_token(token: int):
    query = "select * from my_codes where status='1' and reset_code=:token and expired_in >= now() at time zone 'utc' - interval '10 minutes'"
    return database.fetch_one(query, values={"token": token})


def reset_password(new_password: str, phone_number: int):
    query = "UPDATE my_users SET password=:password WHERE phone_number=:phone_number"
    return database.execute(
        query=query, values={"password": new_password, "phone_number": phone_number}
    )


def disable_reset_code(reset_password_token: int, phone_number: int):
    query = "UPDATE my_codes SET status='9' WHERE status='1' AND reset_code=:reset_code and phone_number=:phone_number"
    return database.execute(
        query, values={"reset_code": reset_password_token, "phone_number": phone_number}
    )


def find_token_logout_lists(token: str):
    query = "select * from my_logoutlists where token=:token"
    return database.fetch_one(query, values={"token": token})
