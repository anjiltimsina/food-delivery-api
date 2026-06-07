from fastapi import APIRouter , Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.schemas.review import ReviewCreate , ReviewResponse
from app.services.review_service import(
    create_review , get_restaurant_reviews , get_my_reviews , delete_review
)
from app.core.dependencies import get_current_customer, get_current_user
from app.models.user import User
from app.utils.pagination  import PaginationParams , paginate
from app.schemas.pagination import PaginatedResponse

router = APIRouter(prefix="/reviews", tags =["Reviews"])

#Public - get all reviews for a restaurant
@router.get("/restaurant/{restaurant_id}", response_model = PaginatedResponse[ReviewResponse])
async def restuarant_reviews(restaurant_id : int , db:AsyncSession = Depends(get_db), pagination: PaginationParams = Depends()):
    reviews = await get_restaurant_reviews(restaurant_id , db)
    return paginate(reviews , pagination)

#customer -get my reviews
@router.get("/my", response_model =PaginatedResponse[ReviewResponse])
async def my_reviews(
    db:AsyncSession = Depends(get_db),
    current_user : User = Depends(get_current_customer),
    pagination : PaginationParams = Depends()
):
    reviews = await get_my_reviews(current_user , db)
    return paginate(reviews , pagination)

#customer-create review (only for delivered orders)
@router.post("/", response_model = ReviewResponse, status_code = 201)
async def create(
    data: ReviewCreate,
    db:AsyncSession = Depends(get_db),
    current_user : User = Depends(get_current_customer)
):
    return await create_review(data , current_user , db)

#ADMIN or OWNER - delete review
@router.delete("/{review_id}")
async def delete( review_id : int , db: AsyncSession = Depends(get_db), current_user : User = Depends(get_current_user) ):
    return await delete_review(review_id , current_user , db)