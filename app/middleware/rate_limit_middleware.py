from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse

#create limite- identifies the users by IP address
limiter = Limiter(key_func = get_remote_address)

#customer error response whern rate limit is exceeded
async def rate_limiter_exceeded_handler(request : Request , exc : RateLimitExceeded):
    return JSONResponse(
        status = 429,
        content ={
            "detail" : "Too many requests .Please slow down and try again later"
        }
    )