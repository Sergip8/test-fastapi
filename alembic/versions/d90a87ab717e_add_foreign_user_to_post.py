"""add foreign_user_to_post

Revision ID: d90a87ab717e
Revises: bd04728bae1a
Create Date: 2023-05-14 17:02:22.911066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd90a87ab717e'
down_revision = 'bd04728bae1a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts',
                           referent_table='users', local_cols=['owner_id'], 
                           remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
