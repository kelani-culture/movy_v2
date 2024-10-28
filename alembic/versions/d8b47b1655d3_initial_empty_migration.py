"""Initial empty migration

Revision ID: d8b47b1655d3
Revises: 246e3f3f22b1
Create Date: 2024-10-28 13:00:58.103971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8b47b1655d3'
down_revision: Union[str, None] = '246e3f3f22b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("seats")
    pass


def downgrade() -> None:
    pass
