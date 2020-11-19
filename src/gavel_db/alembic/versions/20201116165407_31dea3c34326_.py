"""Update problems and solutions

Revision ID: 31dea3c34326
Revises: 78fa69083a7c
Create Date: 2020-11-16 16:54:07.725714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "31dea3c34326"
down_revision = "78fa69083a7c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("problem", sa.Column("domain", sa.VARCHAR(length=4), nullable=True))
    op.add_column("problem", sa.Column("name", sa.VARCHAR(length=100), nullable=True))
    op.drop_column("solution_item", "used")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "solution_item",
        sa.Column("used", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.drop_column("problem", "name")
    op.drop_column("problem", "domain")
    # ### end Alembic commands ###
