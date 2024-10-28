"""Initial empty migration

Revision ID: 5a2613df5f2a
Revises: 66c344ab5a0c
Create Date: 2024-10-28 13:06:41.480160

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a2613df5f2a'
down_revision: Union[str, None] = '66c344ab5a0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("seats")
    pass


def downgrade() -> None:
    pass
