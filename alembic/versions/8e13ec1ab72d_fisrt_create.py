"""fisrt create

Revision ID: 8e13ec1ab72d
Revises: 
Create Date: 2023-05-14 16:02:43.214567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e13ec1ab72d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column(
        'id', sa.Integer(), nullable=False, primary_key=True),sa.Column(
        'title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
