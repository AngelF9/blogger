"""added profile pic

Revision ID: 24b323ffd3bd
Revises: 336b15cd53af
Create Date: 2024-05-23 13:59:08.305628

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "24b323ffd3bd"
down_revision = "336b15cd53af"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("profile_pic", sa.String(length=225), nullable=True)
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("profile_pic")

    # ### end Alembic commands ###
