"""empty message

Revision ID: 9c731605b59a
Revises: f6d5d65a9e7c
Create Date: 2020-08-11 13:54:51.757854

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9c731605b59a'
down_revision = 'f6d5d65a9e7c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pictures')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pictures',
    sa.Column('width', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('height', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('mimetype', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('original', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.Column('recipe_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], name='pictures_recipe_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('width', 'height', 'recipe_id', name='pictures_pkey')
    )
    # ### end Alembic commands ###
