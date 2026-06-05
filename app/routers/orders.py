from fastapi import APIRouter , Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.schemas.order import OrderCreate , OrderResponse , OrderStatusUpdate
from app.services.order_service import (
    place_order , get_my_orders, get_all_orders_admin , get_restaurant_orders , update_order_status , cancel_order, get_order_by_id
)

from app.core.dependencies import(get_current_admin , get_current_customer , get_current_restaurant_owner , get_current_user)
from app.models.user import User

router = APIRouter(prefix ="/orders" , tags =["Orders"])

#customer place order from cart
@router.post("/", response_model = OrderResponse , status_code =201)
async def create_order(
    data: OrderCreate,
    db:AsyncSession = Depends(get_db),
    current_user : User = Depends(get_current_customer)
):
    return await place_order(data, current_user , db)

#customer - view own order
@router.get("/my", response_model = List[OrderResponse])
async def my_orders(db:AsyncSession = Depends(get_db),
                    current_user : User = Depends(get_current_customer)):
    return await get_my_orders(current_user , db)

#Admin view all orders
#Current_user use nabhaye ni authentication ko lagi use bhako ho hai 
@router.get("/all" , response_model = List[OrderResponse])
async def all_orders( db:AsyncSession = Depends(get_db),
                     current_user : User = Depends(get_current_admin)):
    return await get_all_orders_admin(db)


#owner or admin - view restaurant orders

"""
async def get_current_restaurant_owner(
    current_user: User = Depends(
        require_role(UserRole.RESTAURANT_OWNER, UserRole.ADMIN)  # ← BOTH roles allowed
    )
) -> User:
    return current_user
"""
#so restaurant owner handa default mai admin aauxa okay 
@router.get("/restaurant/{restaurant_id}", response_model = List[OrderResponse])
async def restaurant_orders( restaurant_id : int ,
                            db:AsyncSession = Depends(get_db),
                            current_user = Depends(get_current_restaurant_owner)):
    return await get_restaurant_orders(restaurant_id , current_user , db)

#Any auth user - view single order
@router.get("/{order_id}", response_model = OrderResponse)
async def get_order( order_id : int ,
                    db:AsyncSession = Depends(get_db),
                    current_user : User = Depends(get_current_user)):
    return await get_order_by_id(order_id , current_user , db)

#Admin or Owner can update the status
@router.patch("/{order_id}/status" , response_model = OrderResponse)
async def update_status(order_id : int ,
                        data: OrderStatusUpdate,
                        db:AsyncSession = Depends(get_db),
                        current_user : User = Depends(get_current_user)):
    return await update_order_status(order_id , data , current_user , db)

#Customer or Admin  - cancel order
@router.post("/{order_id}/cancel")
async def cancel(order_id : int ,
                 db:AsyncSession,
                 current_user : User = Depends(get_current_user)):
    return await cancel_order(order_id, current_user , db)

    
