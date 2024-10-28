from typing import List

from sqlalchemy.orm import Session

from models.theatre_model import Seat


def generate_theatre_seats(
    db: Session, total_rows: int, seat_per_row: int
) -> List[Seat]:
    """
    generate seat per row for each theatre halls
    """
    seats: List[Seat] = []
    for row_no in range(total_rows):
        row_id = chr(65 + row_no)

        for seat_no in range(1, seat_per_row + 1):
            seat = Seat(row_name=row_id, seat=seat_no)
            seats.append(seat)
    return seats
