from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime,
    MetaData,
    Sequence,
    BIGINT,
)

metadata = MetaData()

users = Table(
    "my_users",
    metadata,
    Column("id", Integer, Sequence("user_id_seq"), primary_key=True),
    Column("email", String(100)),
    Column("password", String(100)),
    Column("fullname", String(50)),
    Column("phone_number", BIGINT),
    Column("state", String(50)),
    Column("city", String(50)),
    Column("created_on", DateTime),
    Column("status", String(1)),
)

codes = Table(
    "my_codes",
    metadata,
    Column("id", Integer, Sequence("code_id_seq"), primary_key=True),
    Column("phone_number", BIGINT),
    Column("reset_code", Integer),
    Column("status", String(1)),
    Column("expired_in", DateTime),
)

logOutlists = Table(
    "my_logoutlists",
    metadata,
    Column("token", String(250), primary_key=True),
    Column("phone_number", BIGINT),
)
