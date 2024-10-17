"""drop casts table

Revision ID: 8d44fee843cf
Revises: e923e3374418
Create Date: 2024-10-17 11:51:15.983486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d44fee843cf'
down_revision: Union[str, None] = 'e923e3374418'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
