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
from app.utils.pagination import paginate, PaginationParams

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
@router.get("/my", response_model = None)
async def my_orders(db:AsyncSession = Depends(get_db),
                    current_user : User = Depends(get_current_customer),
                    pagination : PaginationParams = Depends()):
    orders = await get_my_orders(current_user , db)
    return paginate(orders , pagination)

#Admin view all orders
#Current_user use nabhaye ni authentication ko lagi use bhako ho hai 
@router.get("/all" , response_model = None)
async def all_orders( db:AsyncSession = Depends(get_db),
                     current_user : User = Depends(get_current_admin), 
                     pagination : PaginationParams = Depends()):
    orders = await get_all_orders_admin(db)
    return paginate(orders , pagination)


#owner or admin - view restaurant orders

"""
async def get_current_restaurant_owner(
    current_user: User = Depends(
        require_role(UserRole.RESTAURANT_OWNER, UserRole.ADMIN)  # ← BOTH roles allowed
    )
) -> User:
    return current_user
"""
#so restaurant owner use garda default mai admin aauxa okay 
@router.get("/restaurant/{restaurant_id}", response_model = None)
async def restaurant_orders( restaurant_id : int ,
                            db:AsyncSession = Depends(get_db),
                            current_user = Depends(get_current_restaurant_owner),
                            pagination : PaginationParams = Depends()):
    orders = await get_restaurant_orders(restaurant_id , current_user , db)
    return paginate(orders , pagination)

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
@router.patch("/{order_id}/cancel", response_model = None)
async def cancel(order_id : int ,
                 db:AsyncSession = Depends(get_db),
                 current_user : User = Depends(get_current_user)):
    return await cancel_order(order_id, current_user , db)

    
