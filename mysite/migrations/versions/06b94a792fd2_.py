"""empty message

Revision ID: 06b94a792fd2
Revises: 
Create Date: 2019-05-19 15:14:36.772813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06b94a792fd2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sgb_Assignment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('assignment_name', sa.String(length=150), nullable=True),
    sa.Column('assignment_startdate', sa.DateTime(), nullable=True),
    sa.Column('assignment_duedate', sa.DateTime(), nullable=True),
    sa.Column('assignment_grade', sa.Integer(), nullable=True),
    sa.Column('courses', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['courses'], ['sgb_Course.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sgb_Assignment')
    # ### end Alembic commands ###
