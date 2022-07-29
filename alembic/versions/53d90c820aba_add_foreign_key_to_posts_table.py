"""add foreign-key to posts table

Revision ID: 53d90c820aba
Revises: 49b09dee1aa2
Create Date: 2022-07-26 20:42:17.908989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53d90c820aba'
down_revision = '49b09dee1aa2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    # Remote cols = the column in the referent_table.
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', 
    local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk')
    op.drop_column('posts', 'owner_id')
    pass
