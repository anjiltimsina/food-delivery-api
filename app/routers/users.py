from fastapi import APIRouter , Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import(
    get_all_users , get_user_by_id , update_user , deactivate_user , activate_user
)

from app.core.dependencies import  get_current_user, get_current_admin
from app.models.user import User

router = APIRouter(prefix ="/users", tags = ["Users"])

#Admin only-get all users
@router.get("/", response_model = List[UserResponse])
async def list_users(db:AsyncSession = Depends(get_db),
                     current_user :User = Depends(get_current_admin)):
    return await get_all_users(db)


#Admin only -get any user by id
@router.get("/{user_id}", response_model = UserResponse)
async def get_user(user_id: int ,
                   db: AsyncSession = Depends(get_db),
                   current_user: User = Depends(get_current_admin)):
    return await get_user_by_id(user_id , db)

#Admin or User - Update own profile

#If update is full then we use teh put operation
@router.put("/{user_id}", response_model = UserResponse)
async def update_user_profile( user_id : int ,
                              data : UserUpdate,
                              db:AsyncSession = Depends(get_db),
                              current_user : User = Depends(get_current_user)):
    return await update_user(user_id , data , current_user , db)

#If update is partial then we use the patch
#only admin deactivate the account
@router.patch("/{user_id}/deactivate")
async def activate(
    user_id : int,
    db: AsyncSession = Depends(get_db),
    current_user :User= Depends(get_current_admin)
):
    return await deactivate_user(user_id , db)

# admin only activate the account also
@router.patch("/{user_id}/activate")
async def deactivate(user_id : int,
                   db: AsyncSession = Depends(get_db),
                   current_user : User = Depends(get_current_admin)):
    return await activate_user(user_id , db)

