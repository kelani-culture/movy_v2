"""issued_at nullable

Revision ID: f021c37d240b
Revises: 84ab699d5236
Create Date: 2024-10-29 21:44:07.300458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f021c37d240b'
down_revision: Union[str, None] = '84ab699d5236'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('ticket', 'issued_at',
               existing_type=mysql.DATETIME(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('ticket', 'issued_at',
               existing_type=mysql.DATETIME(),
               nullable=False)
    # ### end Alembic commands ###
