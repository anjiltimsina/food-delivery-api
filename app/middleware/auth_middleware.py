from fastapi import Request
from fastapi.responses import JSONResponse

async def auth_middleware(request: Request , call_next):
    #list of public routes

    public_routes = [
        "/auth/register",
        "/auth/login",
        "auth/refresh",
        "auth/google/login",
        "auth/google/callback",
        "/restaurants",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/"
    ]

    #check if the current path is public
    is_public = any(
        request.url.path.startswith(route)
        for route in public_routes
    )

    if is_public:
        return await call_next(request)
    
    #check if authorization heaer exists
    auth_header = request.headers.get("Authorization")
    #Check if the Authorization header exists
    if not auth_header or not auth_header.startwith("Bearer"):
        return JSONResponse(
            status_code = 401,
            content={"detail": "Authorization header missing or invalid"}
        )
    
    return await call_next(request)

    """
Authentication_header:

Think like this:

When you go to a club:

Door = API endpoint
Bouncer = backend
ID card = Authorization header
    """