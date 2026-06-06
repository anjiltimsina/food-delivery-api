from fastapi import APIRouter , Depends, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.user import UserLogin , UserRegister , UserResponse , TokenResponse
from app.services.auth_service import register_user , login_user , refresh_access_token
from app.core.dependencies import get_current_user
from app.models.user import User
from pydantic import BaseModel, EmailStr
from app.services.google_auth_service import(
    get_google_auth_url , google_login_or_register
)

router = APIRouter(prefix="/auth", tags=["Auth"])

class RefreshRequest(BaseModel):
    refresh_token : str

@router.post("/register", response_model = UserResponse, status_code= 201)
async def register(data: UserRegister, db:AsyncSession= Depends(get_db)):
    user = await register_user(data , db)
    return user

@router.post("/login", response_model = TokenResponse)
async def login (data: UserLogin , db: AsyncSession = Depends(get_db)):
    return await login_user(data, db)

class RefreshRequest(BaseModel):
    refresh_token :str

@router.post("/refresh" , response_model = TokenResponse)
async def refresh(data: RefreshRequest, db:AsyncSession = Depends(get_db)):
    return await refresh_access_token(data.refresh_token, db)

@router.get("/me", response_model = UserResponse)
async def get_me(current_user : User = Depends(get_current_user)):
    return current_user

#Google auth from here 
#step 1
@router.get("/google/login")
async def google_login():
    url = get_google_auth_url()
    return RedirectResponse(url = url) # sends user to Google login page

# step 2
@router.get("/google/callback", response_model =TokenResponse)
async def google_callback(
    code: str = Query(...),
    db:AsyncSession = Depends(get_db)):
    
    return await google_login_or_register(code , db)



