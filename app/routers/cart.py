from fastapi import APIRouter , Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.db.database import get_db
from app.schemas.cart import CartItemAdd , CartItemResponse , CartResponse
from app.services.cart_service import (
    get_cart , add_item_to_cart , remove_item_from_cart , clear_cart , update_cart_item_quantity
)
from app.core.dependencies import get_current_customer
from app.models.user import User


router = APIRouter(prefix ="/cart" , tags=["Cart"])

class UpdateQuantity(BaseModel):
    quantity : int

#Customer - view cart
@router.get("/", response_model = CartResponse)
async def view_cart(
                    db :AsyncSession = Depends(get_db),
                    current_user : User = Depends(get_current_customer)
):
    return await get_cart(current_user , db)

#customer -add item to cart

@router.post("/items", response_model = CartItemResponse, status_code = 201)
async def add_item( data :CartItemAdd,
                   db: AsyncSession = Depends(get_db),
                   current_user :User = Depends(get_current_customer)):
    return await add_item_to_cart(data , current_user , db)

#Customer update item quantity
@router.patch("items/{cart_item_id}", response_model = CartItemResponse)
async def update_quantity( cart_item_id : int,
                          data : UpdateQuantity,
                          db: AsyncSession = Depends(get_db),
                          current_user = Depends(get_current_customer)):
    return update_cart_item_quantity(cart_item_id , data.quantity ,  current_user , db)


# Customer - remove item from cart
@router.delete("items/{cart_item_id}")
async def remove_item( cart_item_id : int ,
                      db:AsyncSession = Depends(get_db),
                      current_user : User  = Depends(get_current_customer)):
    return await remove_item_from_cart(cart_item_id , current_user , db)

#customer - clear entire cart
@router.delete("/")
async def clear( db: AsyncSession = Depends(get_db),
                current_user :User = Depends(get_current_customer)):
    return await clear_cart(current_user , db)

"""
current_user = Depends(get_current_customer)

meaning:

"Before running this route, execute get_current_customer() and store its return value in current_user."

So if get_current_customer() returns a User object, then current_user is that User object. If it raises an exception (for example, invalid token), the route never executes.
"""