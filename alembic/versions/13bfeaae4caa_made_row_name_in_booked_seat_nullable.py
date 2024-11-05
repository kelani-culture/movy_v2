"""made row name in booked seat nullable

Revision ID: 13bfeaae4caa
Revises: 442453d43575
Create Date: 2024-11-05 17:17:47.508983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '13bfeaae4caa'
down_revision: Union[str, None] = '442453d43575'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('seat_booked', 'row_name',
               existing_type=mysql.VARCHAR(length=1),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('seat_booked', 'row_name',
               existing_type=mysql.VARCHAR(length=1),
               nullable=False)
    # ### end Alembic commands ###
