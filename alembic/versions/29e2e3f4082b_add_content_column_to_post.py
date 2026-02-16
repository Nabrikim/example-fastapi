"""add content column to post

Revision ID: 29e2e3f4082b
down_Revision: 4b7228577b09
Create Date: 2026-02-15 13:39:33.885319

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29e2e3f4082b'
down_revision: Union[str, Sequence[str], None] = '4b7228577b09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column("content",sa.String(),nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
