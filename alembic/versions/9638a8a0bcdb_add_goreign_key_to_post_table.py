"""add goreign key to post table

Revision ID: 9638a8a0bcdb
Revises: 9a00e3f36b3b
Create Date: 2026-02-15 14:00:10.083881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9638a8a0bcdb'
down_revision: Union[str, Sequence[str], None] = '9a00e3f36b3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table="posts",referent_table="users",local_cols=["owner_id"],remote_cols=['id'],ondelete="CASCADE")


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column('posts','owner_id')
