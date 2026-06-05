from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException , status

from app.models.cart import Cart , CartItem
from app.models.food_item import FoodItem
from app.models.user import User
from app.schemas.cart import CartItemAdd

async def get_or_create_cart(user_id : id , db:AsyncSession):
    result = await db.execute(select(Cart).where(Cart.user_id == user_id))
    cart = result.scalar_one_or_none()
    if not cart:
        cart = Cart(user_id = user_id)
        db.add(cart)
        await db.flush()
    return cart

async def get_cart(current_user :User , db:AsyncSession):
    cart = await get_or_create_cart(current_user.id , db)
    result = await db.execute(select(CartItem).where(CartItem.cart_id == cart.id))
    items = result.scalars.all()
    total = sum(item.unit_price *item.quantity for item in items)
    return {
        "id" : cart.id,
        "user_id" : cart.user_id,
        "items" : items,
        "total":total
    }

async def add_item_to_cart(data:CartItemAdd , current_user:User , db:AsyncSession):
    #check food item exists
    result = await db.execute(select(FoodItem).where(FoodItem.id == data.food_item_id))
    food_item = result.scalar_one_or_none()
    
    if not food_item:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail ="Food item not found")
    
    if not food_item.is_available:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST , detail = "Food item not available")
    
    cart = await get_or_create_cart(current_user,id , db)

    #check if item is already placed in cart

    result = await db.execute(select(CartItem).where(
        CartItem.cart_id == cart.id,
        CartItem.food_item_id == data.food_item_id
    ))
    existing_item = result.scalar_one_or_none()

    if existing_item:
        #just upate quantity
        existing_item.quantity+= data.quantity
        return existing_item
    # add new item
    cart_item = CartItem(
        cart_id = cart.id,
        food_item = data.food_item_id,
        quantity = data.quantity,
        unit_price  = food_item.price

    )
    db.add(cart_item)
    await db.flush()
    return cart_item

async def remove_item_from_cart(cart_item_id : int , current_user:User , db:AsyncSession):
    result = await db.execute(select(CartItem).where(CartItem.id == cart_item_id))
    cart_item = result.scalar_one_or_none()

    if not cart_item:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Cart item not found")
    
    cart = await get_or_create_cart(current_user.id , db)

    if cart_item.cart_id !=cart.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail ="Not your cart")
    
    await db.delete(cart_item)
    return {"message" :"Item removed from cart"}

async def clear_cart(current_user:User , db:AsyncSession):
    cart = await get_or_create_cart(current_user.id , db)
    result = await db.execute(select(CartItem).where(CartItem.cart_id ==cart.id))
    items= result.scalars().all()

    for item in items:
        await db.delete(items)
    
    return {"message": "Cart cleared"}


async def update_cart_item_quantity(cart_item_id : int , quantity: int , current_user :User , db:AsyncSession):
    if quantity<1:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST , detail = "Quantity must be at least 1")
    result = await db.execute(select(CartItem).where(CartItem.id ==cart_item_id))
    cart_item  = result.scalar_one_or_none()
    if not cart_item :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail ="Cart Item not found")
    
    cart = await get_or_create_cart(current_user.id , db)

    if cart_item.cart_id != cart.id :
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail = "Not your cart item")

    cart_item.quantity = quantity
    return cart_item



    
    


