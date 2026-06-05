from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException , status

from app.models.user import  User
from app.schemas.user import UserRegister , UserLogin , TokenResponse
from app.core.security import hash_password , verify_password , create_access_token, create_refresh_token , decode_token


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
        role = data.role
    )

    db.add(user)
    await db.flush()
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