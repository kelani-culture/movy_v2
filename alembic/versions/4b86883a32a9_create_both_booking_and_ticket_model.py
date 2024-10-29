"""create both booking and ticket model

Revision ID: 4b86883a32a9
Revises: 52d8ed47d191
Create Date: 2024-10-29 17:05:21.474089

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b86883a32a9'
down_revision: Union[str, None] = '52d8ed47d191'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('booking',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
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
    sa.PrimaryKeyConstraint('id', name=op.f('pk_booking'))
    )
    op.create_table('ticket',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('issued_at', sa.DateTime(), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('token', sa.String(length=200), nullable=False),
    sa.Column('booking_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.id'], name=op.f('fk_ticket_booking_id_booking')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_ticket'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ticket')
    op.drop_table('booking')
    # ### end Alembic commands ###
