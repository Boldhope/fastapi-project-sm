"""add content column to posts table

Revision ID: 2bc5007c9344
Revises: d22762dc1008
Create Date: 2022-07-26 20:29:48.963033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bc5007c9344'
down_revision = 'd22762dc1008'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
