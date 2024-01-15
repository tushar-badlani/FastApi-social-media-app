"""Add created add

Revision ID: ba7bb088e62f
Revises: 11432dc5e0c3
Create Date: 2024-01-03 17:32:17.899963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba7bb088e62f'
down_revision: Union[str, None] = '11432dc5e0c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('created_at', sa.DateTime(), nullable=True, server_default="Now()"))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'created_at')
    pass
