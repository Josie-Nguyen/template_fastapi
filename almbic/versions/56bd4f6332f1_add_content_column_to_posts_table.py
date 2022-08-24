"""add content column to posts table

Revision ID: 56bd4f6332f1
Revises: 068cbd79dbd2
Create Date: 2022-08-15 17:43:02.398215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56bd4f6332f1'
down_revision = '068cbd79dbd2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable= False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
