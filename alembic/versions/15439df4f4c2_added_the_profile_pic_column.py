"""added the profile pic column

Revision ID: 15439df4f4c2
Revises: 913ed8e0cf70
Create Date: 2024-10-14 09:32:15.841213

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15439df4f4c2'
down_revision: Union[str, None] = '913ed8e0cf70'
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