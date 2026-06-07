from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException , status

from app.models.review import Review
from app.models.order import Order , OrderStatus
from app.models.user import User , UserRole
from app.schemas.review import ReviewCreate
from app.models.restaurant import Restaurant

async def create_review(data : ReviewCreate , current_user : User , db: AsyncSession):
    #check order exists and belong to the user
    result = await db.execute(select(Order).where(Order.id ==data.order_id))
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail ="Order not found")
    
    #only review if your own orders
    if order.user_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail ="Not your order")
    
    #can only review delivered orders
    if order.status != OrderStatus.DELIVERD:
        raise HTTPException(
            status_code=  status.HTTP_400_BAD_REQUEST,
            detail = "You can only review the delivered orders"
        )
    #check already reviewed
    result = await db.execute(
        select(Review).where(
            Review.order_id == data.order_id,
            Review.user_id == current_user.id))
    
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "You already reviewed this order"
        )

    review = Review(
        user_id = current_user.id ,
        restaurant_id = data.restaurant_id,
        order_id = data.order_id,
        rating = data.rating ,
        comment= data.comment
    )
    db.add(review)

    #update restaurant average rating

    result = await db.execute(
        select(Review).where(Review.restaurant_id == data.restaurant_id)
    )
    all_reviews = result.scalars().all()
    total_rating = sum(r.rating for r in all_reviews) + data.rating
    new_avg = total_rating/(len(all_reviews)+1)

    result = await db.execute(
        select(Restaurant).where(Restaurant.id == data.restaurant_id)
    )
    restaurant = result.scalar_one_or_none()
    if restaurant:
        restaurant.rating = round(new_avg , 2)
    await db.flush()
    return review

async def get_restaurant_reviews(restaurant_id : int , db:AsyncSession):
    result = await db.execute(select(Review).where(Review.restaurant_id ==restaurant_id))
    return result.scalars().all()

async def get_my_reviews(current_user : User , db:AsyncSession):
    result = await db.execute(select(Review).where(Review.user_id == current_user.id))
    return result.scalars().all()

async def delete_review(review_id : int , current_user : User , db:AsyncSession):
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalar_one_or_none()

    if not review:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = "Review not found")
    
    #only admin or review owner can delete
    if current_user.role != UserRole.ADMIN and review.user_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail ="Not allowed")
    
    await db.delete(review)
    return {"message": "Review deleted"}