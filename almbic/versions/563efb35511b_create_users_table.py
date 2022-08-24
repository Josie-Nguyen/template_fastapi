"""create users table

Revision ID: 563efb35511b
Revises: 56bd4f6332f1
Create Date: 2022-08-16 15:33:08.323042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '563efb35511b'
down_revision = '56bd4f6332f1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('create_at', sa.TIMESTAMP(timezone=True),
                                server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
