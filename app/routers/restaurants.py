from fastapi import APIRouter , Depends, HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.schemas.restaurant  import RestaurantCreate , RestaurantUpdate , RestaurantResponse
from app.services.restaurant_service import(
create_restaurant , get_all_restaurants , get_all_restaurants_admin , get_restaurant_by_id , update_restaurant , approve_restaurant , delete_restaurant )

from app.core.dependencies import (
    get_current_admin , get_current_user , get_current_restaurant_owner
)

from app.models import User , UserRole

from app.utils.pagination import PaginationParams , paginate
from app.schemas.pagination import PaginatedResponse
from fastapi import UploadFile , File
from app.utils.upload import save_upload_files , delete_upload_file 


router = APIRouter(prefix= "/restaurants", tags =["Restaurants"])

#Public - anyone can see  all approved restaurants
# so added pagination here
@router.get("/" , response_model = PaginatedResponse[RestaurantResponse])
async def list_restaurants(db: AsyncSession = Depends(get_db),
                           pagination : PaginationParams = Depends()):
    restaurants =  await get_all_restaurants(db)
    return paginate(restaurants , pagination)

#Only admin can see incluing unapprove and inactive
# Added pagination here
@router.get("/admin/all", response_model = PaginatedResponse[RestaurantResponse])
async def list_all_restaurants_admin(db: AsyncSession = Depends(get_db),
                                     current_user: User = Depends(get_current_admin),
                                     pagination : PaginationParams = Depends()):
    restaurants = await get_all_restaurants_admin(db)
    return paginate(restaurants , pagination)

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
@router.patch("/{restaurant_id}/approve", response_model =None)
async def approve(restaurant_id : int ,
                  db:AsyncSession = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    return await approve_restaurant(restaurant_id , db)

#only admin or user can delete the restaurant
@router.delete("/{restaurant_id}", response_model =None)
async def delete(
    restaurant_id : int,
    db:AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await delete_restaurant(restaurant_id , current_user , db)


# Upload Restaurant image
@router.post("/{restaurant_id}/upload-image" , response_model = RestaurantResponse)
async def upload_restaurant_image(
    restaurant_id : int,
    file : UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    restaurant = await get_restaurant_by_id(restaurant_id , db)

    #only owner or admin 
    if current_user.role != UserRole.ADMIN and restaurant.owner_id != current_user.id:
        raise HTTPException(
            status = status.HTTP_403_FORBIDDEN,
            detail = "Not allowed"
        )
    
    #delete old image 
    if restaurant.image and restaurant.image.startswith("uploads"):
        await delete_upload_file(restaurant.image)
    
    #save new image
    image_url = await save_upload_files(file ,"restaurants")
    restaurant.image = image_url 
    return restaurant 

