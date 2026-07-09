from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException , status

from app.models.food_item import FoodItem
from app.models.restaurant import Restaurant
from app.models.user import User , UserRole
from app.schemas.food_item import FoodItemCreate , FoodItemUpdate

async def get_restaurant_or_404(restaurant_id : int , db: AsyncSession):
    result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    restaurant = result.scalar_one_or_none()
    if not restaurant:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = "Restaurant not found")
    return restaurant


async def create_food_item(restaurant_id : int , data : FoodItemCreate , current_user : User , db: AsyncSession):

    restaurant = await get_restaurant_or_404(restaurant_id , db)
    
    if current_user.role != UserRole.ADMIN and restaurant.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN , detail = "Not allowed")
    
    food_item = FoodItem(
        restaurant_id = restaurant_id,
        name  = data.name,
        description = data.description ,
        price = data.price,
        category = data.category
    )

    db.add(food_item)
    await db.flush()
    return food_item

async def get_food_items_by_restaurant(restaurant_id : int , db:AsyncSession):
    await get_restaurant_or_404(restaurant_id , db)
    result = await db.execute(
        select(FoodItem).where(
            FoodItem.restaurant_id == restaurant_id,
            FoodItem.is_available == True))
    return result.scalars().all()

async def get_food_item_by_id(food_item_id: int, db: AsyncSession):
    result = await db.execute(select(FoodItem).where(FoodItem.id == food_item_id))
    food_item = result.scalar_one_or_none()
    if not food_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found")

    # Ensure the parent restaurant is approved and active before exposing this item publicly
    restaurant_result = await db.execute(select(Restaurant).where(Restaurant.id == food_item.restaurant_id))
    restaurant = restaurant_result.scalar_one_or_none()
    if not restaurant or not restaurant.is_active or not restaurant.is_approved:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found")

    return food_item

async def update_food_item(food_item_id :int , data: FoodItemUpdate, current_user : User , db: AsyncSession):
    food_item = await get_food_item_by_id(food_item_id, db)
    restaurant= await get_restaurant_or_404(food_item.restaurant_id , db)
    if current_user.role != UserRole.ADMIN and restaurant.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = "Not allowed")
    
#food item le function bata return bhako food item lai accept garxa jun fooditem return bhathyo tesle chai database access garya thyo 
    if data.name is not None:
        food_item.name = data.name
    
    if data.description is not None:
        food_item.description = data.description
    
    if data.price is not None:
        food_item.price = data.price
    
    if data.category is not None:
        food_item.category = data.category
    
    if data.is_available is not None:
        food_item.is_available = data.is_available
    
    return food_item

async def delete_food_item(food_item_id : int , current_user :User , db:AsyncSession):

    food_item = await get_food_item_by_id(food_item_id, db)
    restaurant = await get_restaurant_or_404(food_item.restaurant_id , db)
    
    if current_user.role != UserRole.ADMIN and restaurant.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = "Not allowed")

    await db.delete(food_item)
    return {"message" : "Food item deleted" }



    