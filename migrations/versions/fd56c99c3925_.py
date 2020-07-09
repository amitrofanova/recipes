"""empty message

Revision ID: fd56c99c3925
Revises: 37e2d45e6055
Create Date: 2020-06-22 12:57:58.584355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd56c99c3925'
down_revision = '37e2d45e6055'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ideas', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'ideas', 'users', ['user_id'], ['id'], ondelete='cascade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ideas', type_='foreignkey')
    op.drop_column('ideas', 'user_id')
    # ### end Alembic commands ###