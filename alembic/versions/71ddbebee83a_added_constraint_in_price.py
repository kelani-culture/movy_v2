"""added constraint in price

Revision ID: 71ddbebee83a
Revises: 33b5e1bd99a4
Create Date: 2024-11-06 12:25:38.040168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71ddbebee83a'
down_revision: Union[str, None] = '33b5e1bd99a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###