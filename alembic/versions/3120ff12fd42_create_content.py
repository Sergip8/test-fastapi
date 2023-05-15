"""create content

Revision ID: 3120ff12fd42
Revises: 8e13ec1ab72d
Create Date: 2023-05-14 16:38:16.907676

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3120ff12fd42'
down_revision = '8e13ec1ab72d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(('content'), sa.String(), nullable=False))
    pass

def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
