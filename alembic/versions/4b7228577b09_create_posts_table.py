"""create posts table

Revision ID: 4b7228577b09
Revises: 
Create Date: 2026-02-15 13:17:36.101745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b7228577b09'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts',sa.Column("id", sa.Integer(), nullable = False,primary_key=True),sa.Column('title',sa.String(),nullable = False))




def downgrade():
    op.drop_table("posts")
