from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException , status

from app.models.user import  User
from app.schemas.user import UserRegister , UserLogin , TokenResponse
from app.core.security import hash_password , verify_password , create_access_token, create_refresh_token , decode_token
from app.utils.email import (
    send_verification_email , send_password_reset_email, create_verification_token, create_password_reset_token
)

async def register_user(data: UserRegister , db:AsyncSession)->User:
    #Check if email already exists
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                            detail = "Email already registered")
    
    result = await db.execute(select(User).where(User.phone == data.phone))
    if result.scalar_one_or_none():
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
                            detail ="Phone number already registered")
    
    user = User(
        full_name = data.full_name,
        email = data.email,
        phone = data.phone,
        hashed_password = hash_password(data.password),
        role = data.role,
        is_verified = False # not verfied yet will be verified ] when we know user has its own email access
    )

    db.add(user)
    await db.flush()

    #send verification email 
    token = create_verification_token(user.email)
    await send_verification_email(user.email , user.full_name , token)
    return user

async def login_user(data: UserLogin , db: AsyncSession) ->TokenResponse:
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password , user.hashed_password):
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail = "Invalid email or password")
    
    if not user.is_active:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Account is deactivated"
        )

    access_token = create_access_token({"sub": str(user.id), "role": user.role})
    refresh_token = create_refresh_token({"sub": str(user.id), "role": user.role})
    
    return TokenResponse(
        access_token = access_token ,
        refresh_token= refresh_token
    )

# refresh garnu parne hunxa ta access token expire bhayesi pheri
async def refresh_access_token(refresh_token : str,db:AsyncSession)->TokenResponse:
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail ="Invalid or expired refresh token"
        )
    
    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "User not found"
        )
    
    access_token = create_access_token({"sub": str(user.id), "role" :user.role})
    new_refresh_token = create_refresh_token({"sub": str(user.id), "role": user.role})

    return TokenResponse(
        access_token = access_token,
        refresh_token=new_refresh_token
    )

#async def refresh_access_token(...) is used when the access token has expired but the refresh token is still valid


async def verify_email(token : str , db:AsyncSession):
    payload= decode_token(token)
    if not payload or payload.get("type") != "verification":
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail = "Invalid or expired verification token"
        )
    
    email = payload.get("sub")
    result = await db.execute(select(User).where(User.email == email))
    user =result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "User not found"
        )
    if user.is_verified:
        return {"message": "Email already verified ! You can login"}
    user.is_verified = True
    return {"message": "Email verified successfully ! You can login. "}


async def forgot_password(email : str , db: AsyncSession):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
 # don't reveal if email exists — security best practice
    if not user :
        return {"message" :"If this email exists, a reset link has been sent"}
    token = create_password_reset_token(user.email)
    await send_password_reset_email(user.email , user.full_name , token)
    return {"message" : "If this email exists, a reset link has been sent"}


async def reset_password(token : str , new_password : str , db: AsyncSession):
    payload = decode_token(token)
    if not payload or payload.get("type") !="password_reset":
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail = "Invalid or expired reset token"
        )
    
    email = payload.get("sub")
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "User not found"
        )
    if len(new_password)<8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Password must be at least 8 characters"
        )
    user.hashed_password=hash_password(new_password)
    return {"message" : "Password reset successfully! You can now login"}
