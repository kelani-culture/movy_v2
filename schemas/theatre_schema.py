from typing import List, Optional

from pydantic import BaseModel, ConfigDict, computed_field, field_validator


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

    model_config = ConfigDict(from_attributes=True)


class TheatreHall(BaseModel):
    name: str
    total_row: int
    seats_per_row: int

    @computed_field
    @property
    def capacity(self) -> int:
        return self.total_row * self.seats_per_row

    @field_validator("total_row", mode="before")
    @classmethod
    def total_row_is_less_than_zero(cls, v: int) -> int:
        if v < 0:
            v = 0
        return v

    @field_validator("seats_per_row", mode="before")
    @classmethod
    def seats_per_row_is_less_than_zero(cls, v: int) -> int:
        if v < 0:
            v = 0
        return v


# theatre movie streaming...
class TheatreMovieStream(BaseModel):
    title: str
    summary: str
    


# theatre hall
class TheatreSeats(BaseModel):
    id: int
    row_name: str
    seat: int


class TheatreHallsResponse(BaseModel):
    id: int
    capacity: int
    seats: List[TheatreSeats]
class TheatreInfo(TheatreResponse):
    theatre_halls: List[TheatreHallsResponse]

    model_config = ConfigDict(from_attributes=True)
