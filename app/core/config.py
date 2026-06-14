#The main purpose of config.py is to act as a central place that reads values from .env and makes them available throughout your application.
#config.py use garepaxi sajilai access garna sakincha we donot need to write os.getenv() every time we want to access a configuration value. Instead, we can simply import the Settings class and create an instance of it to access the values as attributes.
from pydantic_settings import BaseSettings

# yo values haru chai default pass nagare k garne bhanera ho hai
class Settings(BaseSettings):
    APP_NAME : str = "FoodDeliveryAPI"
    DEBUG :bool = False
    SECRET_KEY : str # secret key chai default bhanne hunna birsiyo bhane rakha error aauxa
    ALGORITHM :str ="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES : int =30
    REFRESH_TOKEN_EXPIRE_DAYS : int =7
    DATABASE_URL :str
#Google OAuth
    GOOGLE_CLIENT_ID : str =""
    GOOGLE_CLIENT_SECRET: str =""
    GOOGLE_REDIRECT_URI :str = "http://localhost:8001/auth/google/callback"
#Email 
    MAIL_USERNAME : str  =""
    MAIL_PASSWORD : str = ""
    MAIL_FROM : str = ""
    MAIL_PORT : int = 587
    MAIL_SERVER : str = "smtp.gmail.com"
    MAIL_TLS : bool = True
#TLS means encrypt the conection between backend and gmail
#SSL is another encryption method.
#But: SSL is used with port 465
#TLS is used with port 587
    MAIL_SSL : bool = False

#Stripe integration 
    STRIPE_SECRET_KEY : str = ""
    STRIPE_PUBLISHABLE_KEY : str = ""

    class Config:
        env_file =".env" # yo file location ho jaha bata yo settings haru read garne ho

settings = Settings()