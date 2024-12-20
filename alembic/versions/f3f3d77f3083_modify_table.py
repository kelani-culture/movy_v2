"""modify table

Revision ID: f3f3d77f3083
Revises: 0bf6bf0029aa
Create Date: 2024-10-17 19:37:31.871960

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f3f3d77f3083'
down_revision: Union[str, None] = '0bf6bf0029aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('movie_genres', 'genre_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.alter_column('movie_genres', 'movie_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.create_index(op.f('ixmovies_summary'), 'movies', ['summary'], unique=False, mysql_length=255)
    op.create_index(op.f('ixmovies_tagline'), 'movies', ['tagline'], unique=False)
    op.create_index(op.f('ixmovies_title'), 'movies', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ixmovies_title'), table_name='movies')
    op.drop_index(op.f('ixmovies_tagline'), table_name='movies')
    op.drop_index(op.f('ixmovies_summary'), table_name='movies')
    op.alter_column('movie_genres', 'movie_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.alter_column('movie_genres', 'genre_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
