"""empty message

Revision ID: 5dfad2dac070
Revises: 099e45150de0
Create Date: 2017-12-27 11:21:02.490237

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5dfad2dac070'
down_revision = '099e45150de0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('acess_group', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('isadmin', sa.Boolean(), nullable=True))
    op.drop_constraint('user_ibfk_1', 'user', type_='foreignkey')
    op.create_foreign_key(None, 'user', 'access_group', ['acess_group'], ['id'])
    op.drop_column('user', 'group')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('group', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.create_foreign_key('user_ibfk_1', 'user', 'access_group', ['group'], ['id'])
    op.drop_column('user', 'isadmin')
    op.drop_column('user', 'acess_group')
    # ### end Alembic commands ###
