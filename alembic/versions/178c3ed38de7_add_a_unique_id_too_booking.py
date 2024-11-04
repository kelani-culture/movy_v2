"""add a unique id too booking

Revision ID: 178c3ed38de7
Revises: 1ecb0529f24d
Create Date: 2024-11-04 13:18:03.874389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '178c3ed38de7'
down_revision: Union[str, None] = '1ecb0529f24d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('booking', sa.Column('u_id', sa.String(length=100), nullable=False))
    op.create_unique_constraint(op.f('uq_booking_u_id'), 'booking', ['u_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_booking_u_id'), 'booking', type_='unique')
    op.drop_column('booking', 'u_id')
    # ### end Alembic commands ###
