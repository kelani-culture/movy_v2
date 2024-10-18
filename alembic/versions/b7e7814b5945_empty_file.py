"""empty file

Revision ID: b7e7814b5945
Revises: cb42fa5575da
Create Date: 2024-10-17 19:24:02.380407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7e7814b5945'
down_revision: Union[str, None] = 'cb42fa5575da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
