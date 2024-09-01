"""Add indexes to posts and users

Revision ID: 948a2e970dd2
Revises: 24b323ffd3bd
Create Date: 2024-08-26 11:17:00.479931

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '948a2e970dd2'
down_revision = '24b323ffd3bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_posts_date_posted'), ['date_posted'], unique=False)
        batch_op.create_index(batch_op.f('ix_posts_poster_id'), ['poster_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_posts_slug'), ['slug'], unique=False)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index('email')
        batch_op.drop_index('username')
        batch_op.create_index(batch_op.f('ix_users_date_added'), ['date_added'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_users_username'), ['username'], unique=True)
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', mysql.VARCHAR(length=200), nullable=False))
        batch_op.drop_index(batch_op.f('ix_users_username'))
        batch_op.drop_index(batch_op.f('ix_users_email'))
        batch_op.drop_index(batch_op.f('ix_users_date_added'))
        batch_op.create_index('username', ['username'], unique=True)
        batch_op.create_index('email', ['email'], unique=True)

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_posts_slug'))
        batch_op.drop_index(batch_op.f('ix_posts_poster_id'))
        batch_op.drop_index(batch_op.f('ix_posts_date_posted'))

    # ### end Alembic commands ###