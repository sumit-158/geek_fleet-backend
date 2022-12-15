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
    await crud.save_vendor(user, currentUser.user_id)
    vendor_id = await crud.find_vendor_id(user.vendor_name, user.location)
    await crud.save_review(vendor_id["vendor_id"], review, currentUser.user_id)
    return {**user.dict(), **review.dict()}


@router.patch("/vendor/update/{vendor_id}")
async def update_user(
    vendor_id: str,
    request: schemas.UpdateVendor,
    currentUser: auth_schema.UserList = Depends(jwtUtil.get_current_active_user),
):
    currentVendor = await crud.find_existed_vendor_by_id(vendor_id)
    if not currentVendor:
        raise HTTPException(status_code=404, detail="vendor doesnot extist!")
    currentVendor = schemas.VendorList(**currentVendor)
    # Update user
    await crud.update_vendor(vendor_id, request, currentVendor, currentUser.user_id)
    return {"status_code": 200, "detail": "Vendor updated successfully"}


@router.get("/vendor/profile/{vendor_id}")
async def get_vendor_profile_by_id(vendor_id: str):
    currentVendor = await crud.find_existed_vendor_by_id(vendor_id)

    if not currentVendor:
        raise HTTPException(status_code=404, detail="vendor doesnot extist!")
    currentVendor = schemas.VendorList(**currentVendor)
    return currentVendor


@router.get("/vendor/profile")
async def get_vendor_profile_by_name_loc(vendor_name: str, vendor_location: str):
    currentvendor = await crud.find_existed_vendor(vendor_name, vendor_location)
    if not currentvendor:
        raise HTTPException(status_code=404, detail="vendor doesnot extist!")
    currentvendor = schemas.VendorList(**currentvendor)
    return currentvendor
