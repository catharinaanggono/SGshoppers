"""empty message

Revision ID: 1cb23bad2f39
Revises: 77c80b535da3
Create Date: 2021-10-30 12:58:36.803615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cb23bad2f39'
down_revision = '77c80b535da3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('product_name', sa.String(length=64), nullable=False))
    op.add_column('order', sa.Column('product_image', sa.String(length=64), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'product_image')
    op.drop_column('order', 'product_name')
    # ### end Alembic commands ###
