import time
import logging
from fastapi import Request
#setup logger
logging.basicConfig(level =logging.INFO,
                    format = "%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

async def log_requests(request: Request , call_next):
    start_time = time.time()

    #log incoming requests
    logger.info(f" {request.method} {request.url.path} | IP: {request.client.host}")
    response = await call_next(request)
    #function that passes request to next step (API route)

    #calculate how long it took
    process_time = round(time.time() - start_time *1000 ,2)
    
    #log response
    logger.info( f" {request.method} {request.url.path} |"
                f"Status :{response.status_code} |"
                f"Time :{process_time}ms")
    
    response.headers["X-Process-Time"] = str(process_time)
    return response