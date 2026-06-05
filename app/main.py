from fastapi import FastAPI
from app.routers import auth, users, restaurants, food_items, cart


app = FastAPI(title="FoodDeliveryAPI")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(restaurants.router)
app.include_router(food_items.router)
app.include_router(cart.router)


@app.get("/")
async def root():
    return {"message": "Food Delivery API is running!"}