"""add columns for post table

Revision ID: 1338634d8dd4
Revises: d90a87ab717e
Create Date: 2023-05-14 17:25:20.881149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1338634d8dd4'
down_revision = 'd90a87ab717e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                                     server_default=sa.func.now(), nullable=False))
    op.add_column('posts', sa.Column(('published'), sa.Boolean(), server_default='TRUE', nullable=False))

    pass


def downgrade() -> None:
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')

    pass
