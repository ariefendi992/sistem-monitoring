"""empty message

Revision ID: ea7dd48a9012
Revises: fa0468ac1c65
Create Date: 2023-08-30 19:37:39.148575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea7dd48a9012'
down_revision = 'fa0468ac1c65'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('data_absensi', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pertemuan_Ke', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('data_absensi', schema=None) as batch_op:
        batch_op.drop_column('pertemuan_Ke')

    # ### end Alembic commands ###