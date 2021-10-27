"""empty message

Revision ID: 123a7600c333
Revises: 
Create Date: 2021-10-11 11:01:04.705891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '123a7600c333'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('globaldimension',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('published', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('globaldimensionvalues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('datasetId', sa.Integer(), nullable=False),
    sa.Column('dataset', sa.Text(), nullable=False),
    sa.Column('dimension', sa.Text(), nullable=False),
    sa.Column('globalDimensionId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['globalDimensionId'], ['globaldimension.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('globaldimensionvalues')
    op.drop_table('globaldimension')
    # ### end Alembic commands ###