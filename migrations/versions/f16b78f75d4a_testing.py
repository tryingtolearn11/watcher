"""testing

Revision ID: f16b78f75d4a
Revises: 8a055cef3156
Create Date: 2021-03-29 14:14:59.914093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f16b78f75d4a'
down_revision = '8a055cef3156'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('coin', schema=None) as batch_op:
        batch_op.drop_column('historical_prices_7d_time')
        batch_op.drop_column('historical_prices_7d_prices')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('coin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('historical_prices_7d_prices', sa.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('historical_prices_7d_time', sa.DATETIME(), nullable=True))

    # ### end Alembic commands ###