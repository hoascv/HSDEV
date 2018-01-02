"""empty message

Revision ID: 23c2d659bc33
Revises: 182a0e5f4d06
Create Date: 2017-12-24 14:47:27.310803

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23c2d659bc33'
down_revision = '182a0e5f4d06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('operation', sa.String(length=10), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('logs')
    # ### end Alembic commands ###