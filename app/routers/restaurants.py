from fastapi import APIRouter , Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.schemas.restaurant  import RestaurantCreate , RestaurantUpdate , RestaurantResponse
from app.services.restaurant_service import(
create_restaurant , get_all_restaurants , get_all_restaurants_admin , get_restaurant_by_id , update_restaurant , approve_restaurant , delete_restaurant )

from app.core.dependencies import (
    get_current_admin , get_current_user , get_current_restaurant_owner
)

from app.models import User

router = APIRouter(prefix= "/restaurants", tags =["Restaurants"])

#Public - anyone can see approved restaurants
@router.get("/" , response_model = List[RestaurantResponse])
async def list_restaurants(db: AsyncSession = Depends(get_db)):
    return await get_all_restaurants(db)

#Only admin can see incluing unapprove and inactive
@router.get("/admin/all", response_model = List[RestaurantResponse])
async def list_all_restaurants_admin(db: AsyncSession = Depends(get_db),
                                     current_user: User = Depends(get_current_admin)):
    return await get_all_restaurants_admin(db)

#pulic - all can see by id
@router.get("/{restaurant_id}", response_model = RestaurantResponse)
async def get_restaurant(restaurant_id : int , db:AsyncSession = Depends(get_db)):
    return await get_restaurant_by_id(restaurant_id , db)

#Restaurant-Owner can create
@router.post("/", response_model = RestaurantResponse, status_code = 201)
async def create( data: RestaurantCreate,
                 db:AsyncSession = Depends(get_db),
                 current_user :User = Depends(get_current_restaurant_owner)):
    return await create_restaurant(data , current_user , db)

#owner or Admin can update restaurant
@router.put("/{restaurant_id}", response_model = RestaurantResponse)
async def update(restaurant_id : int ,
                 data: RestaurantUpdate,
                 db:  AsyncSession = Depends(get_db),
                 current_user : User = Depends(get_current_user)):
    return await update_restaurant(restaurant_id , data , current_user , db)

#only admin can approve restaurants
@router.patch("/{restaurant_id}/approve")
async def approve(restaurant_id : int ,
                  db:AsyncSession = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    return await approve_restaurant(restaurant_id , current_user, db)

#only admin or user can delete the restaurant
@router.delete("/{restaurant_id}")
async def delete(
    restaurant_id : int,
    db:AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await delete_restaurant(restaurant_id , current_user , db)


    

