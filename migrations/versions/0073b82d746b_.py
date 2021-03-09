"""empty message

Revision ID: 0073b82d746b
Revises: 04136803554b
Create Date: 2021-03-08 19:08:22.859682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0073b82d746b'
down_revision = '04136803554b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('coin', sa.Column('market_cap_rank', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'coin', ['market_cap_rank'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'coin', type_='unique')
    op.drop_column('coin', 'market_cap_rank')
    # ### end Alembic commands ###