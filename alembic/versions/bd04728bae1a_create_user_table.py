"""create user table

Revision ID: bd04728bae1a
Revises: 3120ff12fd42
Create Date: 2023-05-14 16:47:06.569041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd04728bae1a'
down_revision = '3120ff12fd42'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('email', sa.String(), unique=True, nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
                    )

    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
