from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    DateTime,
    MetaData,
    Sequence,
    BIGINT,
    FLOAT,
    VARCHAR,
)

metadata = MetaData()

users = Table(
    "my_users",
    metadata,
    Column("user_id", String, primary_key=True),
    Column("email", String(100)),
    Column("password", String(100)),
    Column("fullname", String(50)),
    Column("phone_number", BIGINT),
    Column("state", String(50)),
    Column("city", String(50)),
    Column("created_on", DateTime),
    Column("status", String(1)),
)


logOutlists = Table(
    "my_logoutlists",
    metadata,
    Column("token", String(250), primary_key=True),
    Column("phone_number", BIGINT),
)

otps = Table(
    "my_otps",
    metadata,
    Column("id", Integer, Sequence("otp_id_seq"), primary_key=True),
    Column("recipient_id", String(100)),
    Column("session_id", String(100)),
    Column("otp_code", Integer),
    Column("status", String(1)),
    Column("created_on", DateTime),
    Column("updated_on", DateTime),
    Column("otp_failed_count", Integer, default=0),
)

otpBlocks = Table(
    "my_otp_blocks",
    metadata,
    Column("id", Integer, Sequence("otp_block_id_seq"), primary_key=True),
    Column("recipient_id", String(100)),
    Column("created_on", DateTime),
)

vendor = Table(
    "my_vendor",
    metadata,
    Column("vendor_id", String, primary_key=True),
    Column("vendor_name", String(100)),
    Column("location", String(100)),
    Column("description", String(250)),
    Column("morning_timing", FLOAT),
    Column("evening_timing", FLOAT),
    Column("created_by", String),
    Column("last_updated_by", String),
    Column("created_on", DateTime),
    Column("status", String(1)),
)

review = Table(
    "vendor_review",
    metadata,
    Column("id", Integer, Sequence("review_id_seq"), primary_key=True),
    Column("vendor_id", String),
    Column("taste", FLOAT),
    Column("price_to_quality", FLOAT),
    Column("hygiene", FLOAT),
    Column("service", FLOAT),
    Column("created_by", String),
    Column("created_on", DateTime),
    Column("status", String(1)),
)
