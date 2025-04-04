"""empty message

Revision ID: 879fd43eab53
Revises: 6b1f0a752b29
Create Date: 2025-03-29 02:47:46.797363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '879fd43eab53'
down_revision = '6b1f0a752b29'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['uid'], ['person.uid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['uid'], ['planet.uid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('planets')
    op.drop_table('people')
    # ### end Alembic commands ###
