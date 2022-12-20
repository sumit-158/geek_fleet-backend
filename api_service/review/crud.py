from sqlalchemy.orm import Session
from sqlalchemy import and_
import models
from uuid import UUID
from review import schemas
from sqlalchemy.sql import func
from auth import schemas as auth_schema


async def get_review(
    db: Session,
    vendor_id: UUID,
):
    query = db.query(models.Review).filter(
        and_(
            models.Review.vendor_id == vendor_id,
        )
    )
    return query.first()


async def update_review(
    db: Session,
    vendor_id: UUID,
    request: schemas.UpdateReview,
    currentReview: schemas.UpdateReview,
    currentUser: auth_schema.UserList,
):
    query = (
        db.query(models.Review)
        .filter(
            and_(
                models.Review.vendor_id == vendor_id,
                models.Review.created_by == currentUser.user_id,
            )
        )
        .update(
            {
                models.Review.taste: currentReview.taste
                if request.taste is None
                else request.taste,
                models.Review.price_to_quality: currentReview.price_to_quality
                if request.price_to_quality is None
                else request.price_to_quality,
                models.Review.hygiene: currentReview.hygiene
                if request.hygiene is None
                else request.hygiene,
                models.Review.service: currentReview.service
                if request.service is None
                else request.service,
                models.Review.description: currentReview.description
                if request.description is None
                else request.description,
                models.Review.last_updated_on: func.now(),
            }
        )
    )
    db.commit()
    return query


async def delete_review(
    db: Session, vendor_id: UUID, currentUser: auth_schema.UserList
):
    query = (
        db.query(models.Review)
        .filter(
            and_(
                models.Review.vendor_id == vendor_id,
                models.Review.created_by == currentUser.user_id,
            )
        )
        .update({models.Review.status: False})
    )
    db.commit()
    return query
