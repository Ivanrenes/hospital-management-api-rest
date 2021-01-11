"""doctor specialty fixed

Revision ID: 497b5b5b81a8
Revises: a0f1b8665929
Create Date: 2021-01-11 11:27:10.495791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '497b5b5b81a8'
down_revision = 'a0f1b8665929'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Doctors', sa.Column('id_medicalspecialty', sa.Integer(), nullable=True))
    op.drop_column('Doctors', 'id_medicalservice')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Doctors', sa.Column('id_medicalservice', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('Doctors', 'id_medicalspecialty')
    # ### end Alembic commands ###