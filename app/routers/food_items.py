from fastapi import APIRouter , Depends, UploadFile , File , HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.schemas.food_item import FoodItemCreate , FoodItemResponse , FoodItemUpdate
from app.services .food_item_service import(create_food_item , get_food_items_by_restaurant, get_food_item_by_id , update_food_item , delete_food_item, get_restaurant_or_404)
from app.core.dependencies import get_current_restaurant_owner, get_current_user
from app.models.user import User, UserRole
from app.utils.pagination import PaginationParams , paginate
from app.schemas.pagination import PaginatedResponse
from app.utils.upload import save_upload_files , delete_upload_file

router = APIRouter(prefix ="/restaurants", tags=["Food Items"])

#Public - get all food item of a restaurant
#Public - paginate food items
@router.get("/{restaurant_id}/foods" , response_model = PaginatedResponse[FoodItemResponse])
async def list_food_items(restaurant_id : int , db:AsyncSession= Depends(get_db), pagination :PaginationParams = Depends()):
    food_items = await get_food_items_by_restaurant(restaurant_id , db)
    return paginate(food_items , pagination)

#yo pani public nai ho
@router.get("/{restaurant_id}/foods/{food_item_id}", response_model = FoodItemResponse)
async def get_food_item(
    restaurant_id : int,
    food_item_id : int,
    db:AsyncSession = Depends(get_db)
):
    return await get_food_item_by_id(food_item_id, db)

# OWNER or ADMIN - add food item to restaurant
@router.post("/{restaurant_id}/foods" , response_model = FoodItemResponse , status_code =201)
async def add_food_item(
    restaurant_id :int,
    data: FoodItemCreate,
    db:AsyncSession = Depends(get_db),
    current_user :User = Depends(get_current_restaurant_owner)
):
    return await create_food_item(restaurant_id , data , current_user , db)

#Owner or Admin -update food item 
@router.put("/{restaurant_id}/food/{food_item_id}", response_model = FoodItemResponse)
async def update(restaurant_id :int,
                 food_item_id : int ,
                 data:FoodItemUpdate,
                 db:AsyncSession = Depends(get_db),
                 current_user:User = Depends(get_current_user)
                 ):
    return await update_food_item(food_item_id , data , current_user, db)

#Owner or Admin - delete food item
@router.delete("/{restaurant_id}/foods/{food_item_id}")
async def delete(
    restaurant_id:int,
    food_item_id:int,
    db:AsyncSession = Depends(get_db),
    current_user :User = Depends(get_current_user)
):
    return await delete_food_item(food_item_id , current_user , db)

#upload food item image
@router.post("/{restaurant_id}/foods/{food_item_id}/upload-image", response_model = FoodItemResponse)
async def upload_food_item_image(
    restaurant_id : int ,
    food_item_id : int,
    file : UploadFile = File(...),
    db:AsyncSession = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    food_item = await get_food_item_by_id(food_item_id , db)
    restaurant = await get_restaurant_or_404(restaurant_id , db)
    #only owner or admin 

    if current_user.role!= UserRole.ADMIN and restaurant.owner_id != current_user.id:
        raise HTTPException (status_code = status.HTTP_403_FORBIDDEN,
                             detail = "Not allowed")
    #delete old photos
    if food_item.image and food_item.image.startswith("/uploads"):
        await delete_upload_file(food_item.image)

    #save new image
    image_url = await save_upload_files(file , "food-items")
    food_item.image = image_url
    return food_item 
