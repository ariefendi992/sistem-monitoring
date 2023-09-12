"""empty message

Revision ID: 2c81dc977df5
Revises: 9ce2598c18c9
Create Date: 2023-07-10 19:34:16.350196

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2c81dc977df5'
down_revision = '9ce2598c18c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('data_absensi', schema=None) as batch_op:
        batch_op.alter_column('tgl_absen',
               existing_type=mysql.DATETIME(),
               type_=sa.Date(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('data_absensi', schema=None) as batch_op:
        batch_op.alter_column('tgl_absen',
               existing_type=sa.Date(),
               type_=mysql.DATETIME(),
               existing_nullable=True)

    # ### end Alembic commands ###
