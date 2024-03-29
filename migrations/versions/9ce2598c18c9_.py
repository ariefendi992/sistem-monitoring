"""empty message

Revision ID: 9ce2598c18c9
Revises: 147cc7c700dd
Create Date: 2023-09-12 19:06:04.263408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ce2598c18c9'
down_revision = '147cc7c700dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('data_absensi', schema=None) as batch_op:
        batch_op.alter_column('tgl_absen',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('data_absensi', schema=None) as batch_op:
        batch_op.alter_column('tgl_absen',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=True)

    # ### end Alembic commands ###
