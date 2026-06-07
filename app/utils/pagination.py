# This is offset Pagination which i will be doing.
# Pagination is usually applied cause we donot wwant when user hit Get Users , all large dataset is shown in the screen.
#We want limited data response from the user
from fastapi import Query
from typing import Optional

class PaginationParams:
    def __init__(
            self , 
            page: int = Query(default = 1, ge = 1 , description="Page Number"),
            limit : int = Query(default= 10 , ge = 1 , le =100 , description ="Items Per Page")):
        
        self.page = page
        self.limit = limit
        self.offset = (page-1) *limit

def paginate(query_result : list , pagination : PaginationParams)->dict:
    total = len(query_result)
    items = query_result[pagination.offset : pagination.offset+pagination.limit]
    total_pages = (total+pagination.limit -1) //pagination.limit

    return {
        "total" : total,
        "page": pagination.page,
        "limit" : pagination.limit,
        "total_pages" : total_pages,
        "has_next" :pagination.page <total_pages,
        "has_previous" :pagination.page >1,
        "data" : items }
    