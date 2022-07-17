"""Add content column to posts table

Revision ID: 1cf17f125830
Revises: a7be57c3f7c3
Create Date: 2022-07-17 20:57:18.144916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cf17f125830'
down_revision = 'a7be57c3f7c3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
