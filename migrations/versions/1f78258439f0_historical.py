"""historical

Revision ID: 1f78258439f0
Revises: 2f9ec1c407b2
Create Date: 2021-03-21 16:17:24.756837

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f78258439f0'
down_revision = '2f9ec1c407b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('coin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('historical_prices_7d_prices', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('historical_prices_7d_time', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('coin', schema=None) as batch_op:
        batch_op.drop_column('historical_prices_7d_time')
        batch_op.drop_column('historical_prices_7d_prices')

    # ### end Alembic commands ###
