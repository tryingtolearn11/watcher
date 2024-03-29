"""testin

Revision ID: 062a1763298f
Revises: f16b78f75d4a
Create Date: 2021-03-29 14:24:39.856391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '062a1763298f'
down_revision = 'f16b78f75d4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('point',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('x', sa.String(length=32), nullable=True),
    sa.Column('y', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_point'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('point')
    # ### end Alembic commands ###
