from fastapi import APIRouter, Depends, HTTPException
from auth import schemas as auth_schema
from utils import jwtUtil
from review import schemas
from review import crud
from uuid import UUID
from utils.dbUtil import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1")


@router.patch("/review/update")
async def update_review(
    vendor_id: UUID,
    request: schemas.UpdateReview,
    currentUser: auth_schema.UserList = Depends(jwtUtil.get_current_active_user),
    db: Session = Depends(get_db),
):
    review = await crud.get_review(db, vendor_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review doesnot extist!")
    if review.created_by != currentUser.user_id:
        raise HTTPException(status_code=404, detail="No edit right!")
    currentreview = schemas.UpdateReview(
        taste=review.taste,
        price_to_quality=review.price_to_quality,
        hygiene=review.hygiene,
        service=review.service,
        description=review.description,
    )
    # Update user
    await crud.update_review(db, vendor_id, request, currentreview, currentUser)
    return {"status_code": 200, "detail": "Review updated successfully"}


@router.delete("/review")
async def delete_review(
    vendor_id: UUID,
    currentUser: auth_schema.UserList = Depends(jwtUtil.get_current_active_user),
    db: Session = Depends(get_db),
):
    review = await crud.get_review(db, vendor_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review doesnot extist!")
    # Delete user
    await crud.delete_review(db, vendor_id, currentUser)
    return {"status_code": 200, "detail": "Review deleted successfully"}
