"""empty message

Revision ID: f1e5e897965b
Revises: cbb4464195b6
Create Date: 2021-03-10 11:37:29.819005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1e5e897965b'
down_revision = 'cbb4464195b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('coin', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['market_cap_rank'])
        batch_op.create_unique_constraint(None, ['symbol'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('coin', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
