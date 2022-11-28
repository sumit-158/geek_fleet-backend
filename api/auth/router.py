import random
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from api.auth import schemas
from api.auth import crud
from api.utils import cryptoUtil, jwtUtil, constantUtil


router = APIRouter(prefix="/api/v1")


@router.post("/auth/register")
async def register(user: schemas.UserCreate):
    row = await crud.find_existed_user(user.phone_number)
    if row:
        raise HTTPException(status_code=404, detail="User already registered!")

    # Create new user
    user.password = cryptoUtil.get_password_hash(user.password)
    await crud.save_user(user)

    return {**user.dict()}


@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.find_existed_user(int(form_data.username))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user = schemas.UserPWD(**user)
    is_valid = cryptoUtil.verify_password(form_data.password, user.password)
    if not is_valid:
        raise HTTPException(status_code=404, detail="Incorrect username or password")

    access_token_expires = jwtUtil.timedelta(
        minutes=constantUtil.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = await jwtUtil.create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires,
    )

    results = {"access_token": access_token, "token_type": "bearer"}

    results.update({"user_info": {"email": user.email, "fullname": user.fullname}})

    return results


@router.post("/auth/forgot-password")
async def forgot_password(request: schemas.PhoneRequest):
    # Check exited user
    user = await crud.find_existed_user(request.phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create reset code and save it in database
    reset_code = random.randint(1000, 9999)
    await crud.create_reset_code(request, reset_code)

    # Todo setup twiloi service to send eset_code

    return {
        "code": 200,
        "message": "We've sent an email with instructions to reset your password.",
    }


@router.post("/auth/reset-password")
async def reset_password(reset_password_token: int, request: schemas.ResetPassword):
    # Check valid reset password token
    reset_token = await crud.check_reset_password_token(reset_password_token)
    if not reset_token:
        raise HTTPException(
            status_code=404,
            detail="Reset password token has expired, please request a new one.",
        )

    # Check both new & confirm password are matched
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=404, detail="New password is not match.")

    # Reset new password
    code_object = schemas.PhoneRequest(**reset_token)
    new_hash_password = cryptoUtil.get_password_hash(request.new_password)
    await crud.reset_password(new_hash_password, code_object.phone_number)

    # Disable reset code
    await crud.disable_reset_code(reset_password_token, code_object.phone_number)

    return {"code": 200, "message": "Password has been reset successfully"}
