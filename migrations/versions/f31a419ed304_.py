"""empty message

Revision ID: f31a419ed304
Revises: edc7a4e2f018
Create Date: 2017-12-30 19:10:14.270066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f31a419ed304'
down_revision = 'edc7a4e2f018'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('deleted_on', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'deleted_on')
    # ### end Alembic commands ###
