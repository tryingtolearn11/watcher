"""testi

Revision ID: d5395275f616
Revises: 062a1763298f
Create Date: 2021-03-29 14:33:10.265639

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5395275f616'
down_revision = '062a1763298f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('coin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('coin_id_name', sa.String(length=64), nullable=True))
        batch_op.drop_column('coin_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('coin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('coin_id', sa.VARCHAR(length=64), nullable=True))
        batch_op.drop_column('coin_id_name')

    # ### end Alembic commands ###