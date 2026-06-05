from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException , status

from app.models.restaurant import Restaurant
from app.models.user import User , UserRole
from app.schemas.restaurant import RestaurantCreate , RestaurantUpdate

async def create_restaurant(data : RestaurantCreate , current_user : User , db:AsyncSession ):
    # only the restaurant owner can create
    restaurant= Restaurant(
        owner_id = current_user.id,
        name = data.name,
        description = data.description,
        address = data.address,
        phone = data.phone,
        delivery_time = data.delivery_time,
        min_order = data.min_order
    )
    db.add(restaurant)
    await db.flush()
    return restaurant

async def get_all_restaurants(db:AsyncSession):
    result = await db.execute(
        select(Restaurant).where(Restaurant.is_active == True , Restaurant.is_approved == True)
    )
    return result.scalars().all()

#Yesma chai approved nagare ko plus inactive wala pani dekhauxa hai
async def get_all_restaurants_admin(db:AsyncSession):
    result = await db.execute(select(Restaurant))
    return result.scalars().all()

async def get_restaurant_by_id(restaurant_id : int , db:AsyncSession):
    result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    restaurant= result.scalar_one_or_none()
    
    if not restaurant:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Restaurant not found")
    return restaurant


async def update_restaurant(restaurant_id : int , data: RestaurantUpdate, current_user :User , db: AsyncSession):
    restaurant = await get_restaurant_by_id(restaurant_id , db)

    if current_user.role != UserRole.ADMIN and restaurant.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = "Not allowed")
    
    if data.name is not None :
        restaurant.name = data.name
    if data.description is not None:
        restaurant.description = data.description
    if data.address is not None:
        restaurant.address = data.address
    if data.phone is not None:
        restaurant.phone = data.phone
    if data.delivery_time is not None:
        restaurant.delivery_time= data.delivery_time
    if data.min_order is not None:
        restaurant.min_order = data.min_order
    if data.is_active is not None:
        restaurant.is_active = data.is_active

    return restaurant

async def approve_restaurant(restaurant_id : int , db:AsyncSession):
    restaurant = await get_restaurant_by_id(restaurant_id , db)
    restaurant.is_approved = True
    return {"message": f"Restaurant {restaurant.name} approved"}

async def delete_restaurant( restaurant_id : int ,current_user: User , db:AsyncSession ):
    restaurant = await get_restaurant_by_id(restaurant_id , db)
    if current_user != User.ADMIN and restaurant.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = "Not allowed")
    
    await db.delete(restaurant)
    return {"message" : "Restaurant deleted"}








