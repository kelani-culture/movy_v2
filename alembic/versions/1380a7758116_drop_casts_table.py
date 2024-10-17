"""drop casts table

Revision ID: 1380a7758116
Revises: a106eb3f72f7
Create Date: 2024-10-17 11:50:06.053187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1380a7758116'
down_revision: Union[str, None] = 'a106eb3f72f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    op.drop_table("casts")
    pass
