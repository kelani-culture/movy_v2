from typing import List, Optional
from pydantic import BaseModel




class TheatreAddressSchema(BaseModel):
    description: Optional[str]
    street_address: str
    city: str
    state: str



class AddressSchema(BaseModel):
    id: int
    street_address: str
    city: str
    state: str


class TheatreResponse(BaseModel):
    u_id: str
    name: str
    description: str
    addresses: List[AddressSchema]