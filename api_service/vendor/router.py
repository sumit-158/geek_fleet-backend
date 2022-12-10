from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from auth import schemas as auth_schema
from utils import jwtUtil
from vendor import schemas
from vendor import crud

router = APIRouter(prefix="/api/v1")


@router.post("/vendor/register")
async def register(
    user: schemas.RequestVendor,
    review: schemas.RequestReview,
    currentUser: auth_schema.UserList = Depends(jwtUtil.get_current_active_user),
):

    existed_vendor = await crud.find_existed_vendor(user.vendor_name, user.location)
    if existed_vendor:
        raise HTTPException(status_code=404, detail="vendor already registered!")

    # Create vendor
    await crud.save_vendor(user, currentUser.phone_number)
    vendor_id = await crud.find_vendor_id(
        user.vendor_name, user.location, currentUser.phone_number
    )
    await crud.save_review(vendor_id["id"], review, currentUser.phone_number)
    return {**user.dict(), **review.dict()}
    # return vendor_id["id"]
