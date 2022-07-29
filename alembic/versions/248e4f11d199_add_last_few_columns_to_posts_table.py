"""add last few columns to posts table

Revision ID: 248e4f11d199
Revises: 53d90c820aba
Create Date: 2022-07-26 20:47:32.148376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '248e4f11d199'
down_revision = '53d90c820aba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
