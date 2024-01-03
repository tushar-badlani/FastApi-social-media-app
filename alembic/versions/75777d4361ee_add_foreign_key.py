"""Add foreign key

Revision ID: 75777d4361ee
Revises: 66d98c40d3bf
Create Date: 2024-01-03 17:40:39.124160

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '75777d4361ee'
down_revision: Union[str, None] = '66d98c40d3bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fkey', 'posts', 'Users', ['owner_id'], ['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    pass
