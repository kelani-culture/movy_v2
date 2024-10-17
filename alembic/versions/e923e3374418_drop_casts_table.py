"""drop casts table

Revision ID: e923e3374418
Revises: 1380a7758116
Create Date: 2024-10-17 11:50:48.963150

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e923e3374418'
down_revision: Union[str, None] = '1380a7758116'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
