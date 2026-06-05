#This is the file that protects all your routes. Every protected route will use these dependencies.

# Because refresh tokens are only used to generate new access tokens.

"""
{
    "sub": "5",
    "type": "access",
    "exp": 123456789
}
"""

from fastapi import Depends , HTTPException , status
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select 
from app.db.database import get_db
from app.core.security import decode_token 
from app.models.user import User , UserRole

bearer_scheme = HTTPBearer()

#Maybe  token payload looks like:
"""
payload = {
    "sub": "5",
    "type": "access",
    "exp" : 12345678
}
"""

async def get_current_user(
        credentials : HTTPAuthorizationCredentials = Depends(bearer_scheme),
        db:AsyncSession = Depends(get_db)) -> User:
    token = credentials.credentials
    payload = decode_token(token)

    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid or expired token"
        )
    user_id = payload.get("sub")
    if not user_id :
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid token payload"
        )
    result = await db.execute(select(User).where (User.id == int(user_id)  ))
    user = result.scalar_one_or_none()
    #gives the actual User object.
    # user.something garera access garna milyo sab

    if not user :
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Account is deactivated"
        )
    return user

#Role guards


#The * means: Accept any number of roles.
def require_role(*roles : UserRole):
    async def role_checker(current_user : User = Depends(get_current_user))-> User:
        if current_user.role  not in roles :
            raise HTTPException(
                status_code= status.HTTP_403_FORBIDDEN,
                detail = f"Access denied. Required roles : {[r.value for r in roles]}"
            )
        return current_user
    return role_checker

async def get_current_admin(
        current_user : User = Depends(require_role(UserRole.ADMIN))) ->User:
    return current_user

async def get_current_restaurant_owner(current_user : User = Depends(
                                                            require_role(UserRole.RESTAURANT_OWNER , UserRole.ADMIN)
)) -> User:
    return current_user

async def get_current_customer(
        current_user : User = Depends(require_role(UserRole.CUSTOMER , UserRole.ADMIN))
) ->User:
    return current_user


# so yesle chai k help garxa bhanxa kun le kun route chai access garne bhanera
# it is saying admin le access garne customer le ni paunna ra restauarnat owner le pani paunna
# but restaurant owner ra customer le access garna milne sab route chai admin le accesss garxa
    
                                               