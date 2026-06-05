from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException , status
from app.models.order import Order , OrderItem , OrderStatus , PaymentStatus
from app.models.cart import Cart , CartItem 
from app.models.user import User , UserRole
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.models.food_item import FoodItem
from app.models.restaurant import Restaurant

async def place_order(data : OrderCreate , current_user : User , db:AsyncSession):
    # get user cart in order to place the result
    result = await db.execute(select(Cart).where(Cart.user_id == current_user.id))
    cart = result.scalar_one_or_none()

    if not cart:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST , detail = "Cart is empty")
    
    # Aba cart xa bhanne verify bho now we need to take out the cart items 
    result = await db.execute(select(CartItem). where(CartItem.id == cart.id))
    cart_items = result.scalars().all()

    if not cart_items:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST , detail = "Cart is empty")
    
    #all food items must be of same restaurants
    food_items_ids = [item.food_item_id for item in cart_items]
    result = await db.execute(
        select(FoodItem).where(FoodItem.id.in_(food_items_ids))
    )

    food_items = result.scalars().all()
    
    #so jun nun food_items  ko id thyo tesko FoodItem bata list nai aayo
    restaurant_ids = set(f.restaurant_id for f in food_items)
    #restaurant ko id pani aayo an euta matrai restaurant bata order garna milxa so len euta matrai huna parxa yo set ko

    if len(restaurant_ids) >1:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail = "All items must be from teh same restaurant"
        )
    
    restaurant_id = list(restaurant_ids)[0]
    # calculate total 
    total = sum(item.unit_price *item.quantity for item in cart_items)
    #create order
    order = Order(
        user_id = current_user.id,
        restaurant_id = restaurant_id,
        total_amount = total,
        delivery_address = data.delivery_address,
        notes = data.notes,
        status = OrderStatus.PENDING,
        payment_status = PaymentStatus.UNPAID
    )

    db.add(order)
    await db.flush()
#Order place ta bhayo  yeti bhayesi

# but kun kun item ko order bhako ni trace back garnu parxa which are used in many places
    for cart_item in cart_items:
        order_item = OrderItem(
            order_id = order.id,
            food_items_id = cart_item.food_item_id,
            quantity = cart_item.quantity,
            unit_price = cart_item.unit_price)
        
        db.add(order_item)
    
    #clear cart after placing order
    for cart_item in cart_items:
        await db.delete(cart_item)
    await db.flush()
    return order

async def get_my_orders(current_user : User , db: AsyncSession):
    result = await db.execute(select(Order).where(Order.user_id == current_user.id))
    return result.scalars.all()

async def get_order_by_id(order_id : int, current_user : User , db:AsyncSession ):
    result = await db.execute(select(Order).where(Order.id== order_id))
    order = result.scalar_one_or_none()

    if not order:
        raise  HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= "Order not found")

#only admin or order owner can view
    if current_user.role != UserRole.ADMIN and order.user_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN , detail ="Not allowed")
    return order

async def get_all_orders_admin(db:AsyncSession):
    result = await db.execute(select(Order))
    return result.scalars().all()

async def get_restaurant_orders(restaurant_id: int , current_user:User , db: AsyncSession):
    result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    restaurant = result.scalar_one_or_none()

    if not restaurant:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail ="Restaurant not found")
    
    #only owner or admin can see orders
    if current_user.role !=UserRole.ADMIN and restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail ="Not allowed")
    
    result = await db.execute(
        select(Order).where(Order.restaurant_id == restaurant_id)
    )

    return result.scalars().all()

async def update_order_status(order_id : int , data : OrderStatusUpdate , current_user: User , db:AsyncSession):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = "Order not found")
    
    #only admin or restaurant owner can update status
    if current_user.role != UserRole.ADMIN:
        result = await db.execute(select(Restaurant).where(Restaurant.id ==order.restaurant ))
        restaurant = result.scalar_one_or_none()
        if not restaurant or restaurant.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail ="Not allowed")
    
    order.status = data.status
    return order

async def cancel_order(order_id : int , current_user : User , db:AsyncSession):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail = "Order not found")
    
    if current_user.role != UserRole.ADMIN and order.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN , detail ="Not allowed")
    
    #can cancel only if pending
    if order.status != OrderStatus.PENDING:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail = f"Cannot cancel order with status {order.status.value}"
        )
        
    order.status = OrderStatus.CANCELLED
    return {"message", "Order cancelled successfully"}





