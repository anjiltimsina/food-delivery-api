import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException , status
import random
from app.models import User , UserRole
from app.core.security import create_access_token , create_refresh_token
from app.core.config import settings
from app.schemas.user import TokenResponse
from urllib.parse import urlencode

#client id : Tells Google which application is making the request.
#client_secret : Proves your backend is really your backend.
#Google verifies: Yes, this is the owner of App #123

#step 1 : Buil the Google Login URL 
# we send user to this URL to login with Google 

def get_google_auth_url() -> str:
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id" : settings.GOOGLE_CLIENT_ID,
        "redirect_uri" : settings.GOOGLE_REDIRECT_URI,
        "response_type":"code", # Google will send back a code
        "scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile", # we want email and profile info
        "access_type" : "offline", #Allows Google to provide a refresh token if needed.
        "prompt" : "consent" #Forces Google's consent screen.
    }

    return f"{base_url}?{urlencode(params)}"

#step 2 - Exchange the "code" for an access token 
#Google gave us a code, now we have to exchange it for a actual user info
async def exchange_code_for_token(code : str) ->dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://oauth2.googleapis.com/token",
            data ={
                "code" : code,
                "client_id" : settings.GOOGLE_CLIENT_ID,
                "client_secret" : settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri" :settings.GOOGLE_REDIRECT_URI,
                "grant_type" : "authorization_code"
            })
        
        if response.status_code != 200:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Failed to exchange code for token"
            )
        return response.json()

#so in upper code if everything valid it returns

#step 3: get user info from teh Google
async def get_google_user_info(access_token: str) ->dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers = {"Authorization" : f"Bearer {access_token}"})
        
        if response.status_code !=200:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Failed to get user info from the Google")
        
        return response.json()
        # returns something like:
    # {
    #   "id": "1234567890",
    #   "email": "user@gmail.com",
    #   "name": "John Doe",
    #   "picture": "https://..."
    # }

#step 4 - login or register the user
# if the user exists - login  , if not - create new token
async def google_login_or_register(code : str , db:AsyncSession) ->TokenResponse:
    #exchange code from google

    token_data = await exchange_code_for_token(code)
    access_token = token_data.get("access_token")

    if not access_token:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "No access token from Google"
        )

    # get user info from the google 

    #get user info from the google
    google_user = await get_google_user_info(access_token)

    email = google_user.get("email")
    full_name = google_user.get("name")
    profile_picture = google_user.get("picture")

    if not email:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail = "Couldnot get email from google"
        )
    #check if user already exists in our database
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user:
        # user exists: just login
        if not user.is_active:
            raise HTTPException(
                status_code= status.HTTP_403_FORBIDDEN,
                detail = "Account is deactivated"
            )
        #update profile picture if changed
        if profile_picture:
            user.profile_image = profile_picture
    else:
        fake_phone = f"google_{random.randint(1000000000, 9999999999)}"

        user = User(
            full_name = full_name,
            email =email,
            phone = fake_phone,
            hashed_password = "", # no password for google user
            role = UserRole.CUSTOMER,
            is_active = True,
            is_verified =  True,
            profile_image = profile_picture)
        
        db.add(user)
        await db.flush()

    #generate our JWT tokens
    our_access_token = create_access_token({"sub": str(user.id), "role": user.role})
    our_refresh_token = create_refresh_token({"sub": str(user.id), "role": user.role})

    return TokenResponse(
        access_token= our_access_token,
        refresh_token= our_refresh_token
    )









#Complete workflow
"""
1. User clicks Login with Google
                ↓
2. Google Login Page
                ↓
3. User logs in
                ↓
4. Google redirects back

   /callback?code=ABC123

                ↓
5. exchange_code_for_token()

   sends ABC123 to Google

                ↓
6. Google returns

   access_token
  

                ↓
7. Decode access_token

   email
   name
   picture

                ↓
8. Find/Create user in DB

                ↓
9. Generate YOUR JWT

                ↓
10. Return JWT to frontend
"""



