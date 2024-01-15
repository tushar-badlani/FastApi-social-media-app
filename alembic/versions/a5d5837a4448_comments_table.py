"""Comments_table

Revision ID: a5d5837a4448
Revises: b3f467e5a626
Create Date: 2024-01-15 21:37:16.841712

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5d5837a4448'
down_revision: Union[str, None] = 'b3f467e5a626'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('commented_on_id', sa.Integer(), nullable=True))
    op.create_foreign_key('posts_posts_fkey', 'posts', 'posts', ['commented_on_id'], ['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_column('posts', 'commented_on_id')
    op.drop_constraint('posts_posts_fkey', 'posts', type_='foreignkey')
    pass
