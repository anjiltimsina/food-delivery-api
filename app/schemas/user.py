from pydantic import BaseModel , EmailStr , field_validator
from app.models import UserRole
from typing import Optional

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    password: str
    role: UserRole = UserRole.CUSTOMER

    @field_validator("password")
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least of 8 characters")
        return v

    @field_validator("phone")
    def phone_valid(cls, v):
        if not v.replace("+", "").isdigit():
            raise ValueError("Invalid Phone Number")
        return v

    @field_validator("role")
    def restrict_public_roles(cls, v):
        allowed_roles = {UserRole.CUSTOMER, UserRole.RESTAURANT_OWNER}
        if v not in allowed_roles:
            raise ValueError("Invalid role. Allowed roles are: customer, restaurant_owner")
        return v
    
class UserLogin(BaseModel):
    email: EmailStr
    password:str


class UserResponse(BaseModel):
    id: int
    full_name : str
    phone: str
    role:UserRole
    is_active : bool
    is_verified: bool
    profile_image : Optional[str] = None
    model_config ={"from attributes": True}

# Yesto k like update ma harek kura update garna parxa bhanne xaina ni ta choice hunxa so all Optional xa change nagare None pass hunxa

class UserUpdate(BaseModel):
    full_name :Optional[str] = None
    phone:Optional[str] =None
    profile_image: Optional[str] =None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token : str
    token_type : str = "bearer"
