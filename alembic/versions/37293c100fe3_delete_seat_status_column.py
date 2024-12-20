"""delete seat status column

Revision ID: 37293c100fe3
Revises: d90379dbdf54
Create Date: 2024-10-29 16:33:06.484020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '37293c100fe3'
down_revision: Union[str, None] = 'd90379dbdf54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('seats', 'status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seats', sa.Column('status', mysql.ENUM('AVAILABLE', 'RESERVED', 'BOOKED'), nullable=False))
    # ### end Alembic commands ###
