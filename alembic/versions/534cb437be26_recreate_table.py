"""recreate table

Revision ID: 534cb437be26
Revises: aa714218cab6
Create Date: 2024-11-05 18:14:30.031881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '534cb437be26'
down_revision: Union[str, None] = 'aa714218cab6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('theatre_halls',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.Column('total_row', sa.Integer(), nullable=False),
    sa.Column('seats_per_row', sa.Integer(), nullable=False),
    sa.Column('theatre_id', sa.String(length=100), nullable=False),
    sa.CheckConstraint('seats_per_row >= 0', name='check_seats_per_row_non_negative'),
    sa.CheckConstraint('total_row >= 0', name='check_total_rows_non_negative'),
    sa.ForeignKeyConstraint(['theatre_id'], ['theatres.id'], name=op.f('fk_theatre_halls_theatre_id_theatres')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_theatre_halls')),
    sa.UniqueConstraint('name', name=op.f('uq_theatre_halls_name'))
    )
    op.create_table('seat_booked',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('available_seats', sa.Integer(), nullable=True),
    sa.Column('theatrehall_id', sa.Integer(), nullable=False),
    sa.Column('added_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['theatrehall_id'], ['theatre_halls.id'], name=op.f('fk_seat_booked_theatrehall_id_theatre_halls')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_seat_booked'))
    )
    op.create_table('seats',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('row_name', sa.String(length=1), nullable=False),
    sa.Column('seat', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('AVAILABLE', 'RESERVED', 'BOOKED', name='seatstatus'), nullable=False),
    sa.Column('theatre_hall_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['theatre_hall_id'], ['theatre_halls.id'], name=op.f('fk_seats_theatre_hall_id_theatre_halls')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_seats')),
    sa.UniqueConstraint('row_name', 'seat', 'theatre_hall_id', name='uq_theatre_hall_id_row_name_seat_row')
    )
    op.create_table('show_time',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('u_id', sa.String(length=100), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('theatre_hall_id', sa.Integer(), nullable=False),
    sa.Column('stream_date', sa.Date(), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], name=op.f('fk_show_time_movie_id_movies')),
    sa.ForeignKeyConstraint(['theatre_hall_id'], ['theatre_halls.id'], name=op.f('fk_show_time_theatre_hall_id_theatre_halls')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_show_time')),
    sa.UniqueConstraint('u_id', name=op.f('uq_show_time_u_id'))
    )
    op.create_table('booking',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('u_id', sa.String(length=100), nullable=False),
    sa.Column('booking_status', sa.String(length=8), nullable=False),
    sa.Column('showtime_id', sa.Integer(), nullable=False),
    sa.Column('seat_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=100), nullable=False),
    sa.Column('theatre_hall_id', sa.Integer(), nullable=False),
    sa.Column('added_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['seat_id'], ['seats.id'], name=op.f('fk_booking_seat_id_seats')),
    sa.ForeignKeyConstraint(['showtime_id'], ['show_time.id'], name=op.f('fk_booking_showtime_id_show_time')),
    sa.ForeignKeyConstraint(['theatre_hall_id'], ['theatre_halls.id'], name=op.f('fk_booking_theatre_hall_id_theatre_halls')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_booking_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_booking')),
    sa.UniqueConstraint('u_id', name=op.f('uq_booking_u_id'))
    )
    op.create_table('booking_seat',
    sa.Column('seat_id', sa.Integer(), nullable=True),
    sa.Column('booking_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.id'], name=op.f('fk_booking_seat_booking_id_booking')),
    sa.ForeignKeyConstraint(['seat_id'], ['seats.id'], name=op.f('fk_booking_seat_seat_id_seats'))
    )
    op.create_table('ticket',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('issued_at', sa.DateTime(), nullable=True),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('token', sa.String(length=200), nullable=True),
    sa.Column('booking_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.id'], name=op.f('fk_ticket_booking_id_booking')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_ticket'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ticket')
    op.drop_table('booking_seat')
    op.drop_table('booking')
    op.drop_table('show_time')
    op.drop_table('seats')
    op.drop_table('seat_booked')
    op.drop_table('theatre_halls')
    # ### end Alembic commands ###
