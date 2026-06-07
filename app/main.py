from fastapi import FastAPI
from app.routers import auth, users, restaurants, food_items, cart, food_items, reviews, orders
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi.errors import RateLimitExceeded
import os
from app.middleware.logging_middleware import log_requests
from app.middleware.auth_middleware import auth_middleware
from app.middleware.rate_limit_middleware import Limiter, rate_limiter_exceeded_handler 
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="FoodDeliveryAPI")

#serve the uploaded files as static
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads" , StaticFiles(directory= "uploads") , name ="uploads")
# Fastapi knows about the route only but not folder named exists.
# Whenever someone requests /uploads/..., look inside the local uploads/ folder and serve that file.


#Rate Limiter setup
app.state.limiter = Limiter
app.add_exception_handler(RateLimitExceeded, rate_limiter_exceeded_handler)

#--CORS Middleware--
#allows your frontend (React) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins =["*"], # in production put your frontend URL here # Allow requests from ANY website.
    allow_credentials = True,
    allow_methods =["*"],
    allow_headers=["*"]
)

"""
allow_credentials=True

Allows:
Cookies
Authorization headers
Sessions
"""


"""
Allow methods are :

GET
POST
PUT
PATCH
DELETE
"""


#---Logging Middleware -- 
app.add_middleware(BaseHTTPMiddleware , dispatch = log_requests)

#---Auth Middleware---
app.add_middleware(BaseHTTPMiddleware , dispatch = auth_middleware)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(restaurants.router)
app.include_router(food_items.router)
app.include_router(cart.router)
app.include_router(reviews.router)
app.include_router(orders.router)

@app.get("/")
async def root():
    return {"message": "Food Delivery API is running!"}