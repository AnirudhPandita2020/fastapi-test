"""add last column

Revision ID: f057b9c2a341
Revises: 065b9f2155b4
Create Date: 2022-03-04 11:46:53.193057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f057b9c2a341'
down_revision = '065b9f2155b4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('userid',sa.Integer(),nullable=False))
    


def downgrade():
    op.drop_column('posts','userid')
