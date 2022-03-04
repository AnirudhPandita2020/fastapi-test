"""create all tables

Revision ID: 065b9f2155b4
Revises: 
Create Date: 2022-03-04 01:49:47.858776

"""
from cgitb import text
from time import time
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '065b9f2155b4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',sa.Column('email',sa.String(),nullable=False,unique=True),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('userid',sa.Integer(),primary_key=True,nullable=False,autoincrement=True),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')))
    op.create_table('posts',sa.Column('id',sa.Integer(),primary_key=True,nullable=False,autoincrement=True)
                    ,sa.Column('title',sa.String(),nullable=False)
                    ,sa.Column('content',sa.String(),nullable=False)
                    ,sa.Column('published',sa.Boolean(),server_default='True',nullable=False)
                    ,sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')))
                    
    
    op.create_table('votes',sa.Column('user_id',sa.Integer(),sa.ForeignKey('users.userid',ondelete="CASCADE"),primary_key=True),
                    sa.Column('post_id',sa.Integer(),sa.ForeignKey("posts.id",ondelete="Cascade"),primary_key=True))


def downgrade():
    op.drop_table('posts')
    op.drop_table('users')
    op.drop_table('votes')
