from utils.dbUtil import database
from vendor import schemas
import datetime


def save_vendor(user: schemas.RequestVendor, creator: int):
    query = "INSERT INTO my_vendor VALUES (:id ,:vendor_name, :location, :description, :morning_timing, :evening_timing, :created_by, now() at time zone 'UTC', '1')"
    return database.execute(
        query,
        values={
            "id": str(str(datetime.datetime.now()) + user.vendor_name[:4]),
            "vendor_name": user.vendor_name,
            "location": user.location,
            "description": user.description,
            "morning_timing": user.morning_timing,
            "evening_timing": user.evening_timing,
            "created_by": creator,
        },
    )


def find_existed_vendor(vendor_name: str, location: str):
    query = "select * from my_vendor where vendor_name=:vendor_name and location=:location and status='1'"
    return database.fetch_one(
        query, values={"vendor_name": vendor_name, "location": location}
    )


def find_vendor_id(vendor_name: str, location: str, creator: int):
    query = "select id from my_vendor where vendor_name=:vendor_name and location=:location and created_by=:creator and status='1'"
    return database.fetch_one(
        query,
        values={"vendor_name": vendor_name, "location": location, "creator": creator},
    )


def save_review(vendor_id: str, reviews: schemas.RequestReview, creator: int):
    query = "INSERT INTO vendor_review VALUES (nextval('review_id_seq'), :vendor_id, :taste, :price_to_quality, :hygiene, :service, :created_by, now() at time zone 'UTC', '1')"
    return database.execute(
        query,
        values={
            "vendor_id": vendor_id,
            "taste": reviews.taste,
            "price_to_quality": reviews.price_to_quality,
            "hygiene": reviews.hygiene,
            "service": reviews.service,
            "created_by": creator,
        },
    )
