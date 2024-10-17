from typing import Dict

from sqlalchemy.orm import Session

from models.theatre_model import Address, Theatre


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
