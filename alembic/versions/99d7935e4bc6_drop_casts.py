"""drop casts

Revision ID: 99d7935e4bc6
Revises: eaa06a9da5ae
Create Date: 2024-10-17 12:00:29.829267

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99d7935e4bc6'
down_revision: Union[str, None] = 'eaa06a9da5ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
