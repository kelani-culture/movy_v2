"""drop casts

Revision ID: eaa06a9da5ae
Revises: 8d44fee843cf
Create Date: 2024-10-17 11:51:30.892516

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eaa06a9da5ae'
down_revision: Union[str, None] = '8d44fee843cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
