"""Add user table

Revision ID: 66d98c40d3bf
Revises: ba7bb088e62f
Create Date: 2024-01-03 17:36:12.640714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66d98c40d3bf'
down_revision: Union[str, None] = 'ba7bb088e62f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('Users',sa.Column('id',sa.Integer(),nullable=False, primary_key=True), sa.Column('email',sa.String(),nullable=False), sa.Column('password',sa.String(),nullable=False), sa.Column('created_at',sa.DateTime(),nullable=True, server_default="Now()"), sa.UniqueConstraint('email', name='unique_email'))
    pass


def downgrade() -> None:
    op.drop_table('Users')
    pass
