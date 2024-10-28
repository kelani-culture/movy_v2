from typing import Dict

from sqlalchemy.orm import Session

from models.theatre_model import Address, Theatre, TheatreHall
from utils.create_seats import generate_theatre_seats


def create_theatre_address(
    db: Session, data: Dict[str, str], theatre: Theatre
) -> Theatre:
    """
    handles user theatre address creation
    """
    description = data.pop("description")
    address = Address(**data)
    db.add(address)

    theatre.description = description
    theatre.addresses.append(address)
    db.commit()

    db.refresh(theatre)

    return theatre


def create_theatre_halls_seats(
    db: Session, data: Dict[str, int | str], theatre: Theatre
):
    """
    create user theatre halls and seats
    """
    theatre_hall = TheatreHall(**data)
    db.add(theatre_hall)

    theatre.theatre_halls.append(theatre_hall)

    total_row = data["total_row"]
    seats_per_row = data["seats_per_row"]
    seats = generate_theatre_seats(db, total_row, seats_per_row)

    theatre_hall.seats.extend(seats)
    db.add_all(seats)
    db.commit()


def get_theatre_detail(db: Session, theatre: Theatre):
    """
    get all full detail on theatre
    """
    return db.query(Theatre).filter(Theatre.id == theatre.id).first()
