from uuid import uuid4
from utils.dbUtil import database
from vendor import schemas
from auth import schemas as auth_schema


def save_vendor(user: schemas.RequestVendor, creator: str):
    query = "INSERT INTO my_vendor VALUES (:vendor_id,:vendor_name, :location, :description, :morning_timing, :evening_timing, :created_by, :last_updated_by, now() at time zone 'UTC', '1')"
    return database.execute(
        query,
        values={
            "vendor_id": str(uuid4()),
            "vendor_name": user.vendor_name,
            "location": user.location,
            "description": user.description,
            "morning_timing": user.morning_timing,
            "evening_timing": user.evening_timing,
            "created_by": creator,
            "last_updated_by": creator,
        },
    )


def find_existed_vendor(vendor_name: str, location: str):
    query = "select * from my_vendor where vendor_name=:vendor_name and location=:location and status='1'"
    return database.fetch_one(
        query, values={"vendor_name": vendor_name, "location": location}
    )


def find_existed_vendor_by_id(vendor_id: str):
    query = "select * from my_vendor where vendor_id=:vendor_id and status='1'"
    return database.fetch_one(query, values={"vendor_id": vendor_id})


def find_vendor_id(vendor_name: str, location: str):
    query = "select vendor_id from my_vendor where vendor_name=:vendor_name and location=:location and status='1'"
    return database.fetch_one(
        query,
        values={"vendor_name": vendor_name, "location": location},
    )


def save_review(vendor_id: str, reviews: schemas.RequestReview, creator: str):
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


def update_vendor(
    vendor_id: str,
    request: schemas.UpdateVendor,
    currentVendor: schemas.UpdateVendor,
    currentUser: str,
):
    query = "UPDATE my_vendor SET vendor_name=:vendor_name, location=:location, description=:description, morning_timing=:morning_timing, evening_timing=:evening_timing, last_updated_by=:last_updated_by where vendor_id=:vendor_id"
    return database.execute(
        query,
        values={
            "vendor_name": currentVendor.vendor_name
            if request.vendor_name is None
            else request.vendor_name,
            "location": currentVendor.location
            if request.location is None
            else request.location,
            "description": currentVendor.description
            if request.description is None
            else request.description,
            "morning_timing": currentVendor.morning_timing
            if request.morning_timing is None
            else request.morning_timing,
            "evening_timing": currentVendor.evening_timing
            if request.evening_timing is None
            else request.evening_timing,
            "last_updated_by": currentUser,
            "vendor_id": vendor_id,
        },
    )
