from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException , status
from app.models.user import User , UserRole
from app.schemas.user import UserUpdate

async def get_all_users(db:AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()

async def get_user_by_id(user_id : int , db:AsyncSession):
    result = await db.execute(select(User).where (User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail = "User not found")
    return user

async def update_user(user_id : int , data:UserUpdate , current_user : User , db:AsyncSession):
# only admin or the user themselves can update
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN , detail = "Not allowed")
     
    user = await get_user_by_id(user_id , db)

    if data.full_name:
        user.full_name = data.full_name

    if data.phone:
        user.phone = data.phone
    if data.profile_image:
        user.profile_image = data.profile_image

    return user

async def deactivate_user(user_id : int , db: AsyncSession):
    user = await get_user_by_id(user_id , db)
    user.is_active = False
    return {"message": f"User {user.full_name} deactivated"}

async def activate_user(user_id : int , db: AsyncSession):
    user = await get_user_by_id(user_id , db)
    user.is_active = True
    return {"message": f"User {user.full_name} activated"}
    