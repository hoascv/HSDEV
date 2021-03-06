"""empty message

Revision ID: edc7a4e2f018
Revises: 5dfad2dac070
Create Date: 2017-12-30 18:51:49.328038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edc7a4e2f018'
down_revision = '5dfad2dac070'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('deleted_on', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'deleted_on')
    # ### end Alembic commands ###
