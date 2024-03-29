"""empty message

Revision ID: f12a405284b1
Revises: f9d7b75c66d6
Create Date: 2023-08-23 17:33:10.125682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f12a405284b1"
down_revision = "f9d7b75c66d6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("data_pelanggaran", schema=None) as batch_op:
        batch_op.add_column(sa.Column("guru_id", sa.Integer(), nullable=False))
        batch_op.create_foreign_key(
            None,
            "detail_guru",
            ["guru_id"],
            ["user_id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("data_pelanggaran", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_column("guru_id")

    # ### end Alembic commands ###
