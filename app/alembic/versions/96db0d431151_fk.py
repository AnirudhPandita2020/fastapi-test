"""fk

Revision ID: 96db0d431151
Revises: f057b9c2a341
Create Date: 2022-03-04 11:52:32.683102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96db0d431151'
down_revision = 'f057b9c2a341'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key('post_user_fk','posts','users',local_cols=['userid'],remote_cols=['userid'],ondelete="CASCADE")


def downgrade():
    op.drop_constraint('posts_user_fk','posts',type_="foreignkey")
