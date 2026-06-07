# pagination le chai dictionary return garxa tara response model le expects a plain lists . so conflicts occurs
# so response_model = None halda chai we donot have control over what is being out yeah
# so let us make the paginateresponse schema 

from pydantic import BaseModel
from typing import Generic , TypeVar , List

T= TypeVar("T")

class PaginatedResponse(BaseModel , Generic[T]):
    total : int
    page:int
    limit:int
    total_pages : int
    has_next : bool
    has_previous:bool
    data:List[T]