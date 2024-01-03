"""Create_post_table

Revision ID: 11432dc5e0c3
Revises: 
Create Date: 2024-01-03 17:23:00.872913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11432dc5e0c3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False, primary_key=True), sa.Column('title',sa.String(),nullable=False), sa.Column('content',sa.String(),nullable=False), sa.Column('published',sa.Boolean(),server_default='True',nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
