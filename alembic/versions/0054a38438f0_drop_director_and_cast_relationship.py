"""drop director and cast relationship

Revision ID: 0054a38438f0
Revises: 7b9cd24c6e46
Create Date: 2024-10-17 17:45:28.697144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '0054a38438f0'
down_revision: Union[str, None] = '7b9cd24c6e46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movie_casts')
    op.drop_table('movie_directors')
    op.add_column('movies', sa.Column('tagline', sa.String(length=50), nullable=True))
    op.drop_index('ixmovies_tag_line', table_name='movies')
    op.create_index(op.f('ixmovies_tagline'), 'movies', ['tagline'], unique=False)
    op.drop_column('movies', 'tag_line')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies', sa.Column('tag_line', mysql.VARCHAR(length=50), nullable=True))
    op.drop_index(op.f('ixmovies_tagline'), table_name='movies')
    op.create_index('ixmovies_tag_line', 'movies', ['tag_line'], unique=False)
    op.drop_column('movies', 'tagline')
    op.create_table('movie_directors',
    sa.Column('director_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('movie_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['director_id'], ['directors.id'], name='fk_movie_directors_director_id_directors'),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], name='fk_movie_directors_movie_id_movies'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('movie_casts',
    sa.Column('cast_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('movie_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['cast_id'], ['casts.id'], name='fk_movie_casts_cast_id_casts'),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], name='fk_movie_casts_movie_id_movies'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
