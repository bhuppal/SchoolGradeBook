"""empty message

Revision ID: aca9623c3b60
Revises: 06b94a792fd2
Create Date: 2019-05-19 19:41:49.582040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aca9623c3b60'
down_revision = '06b94a792fd2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sgb_Student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.String(length=150), nullable=True),
    sa.Column('first_name', sa.String(length=150), nullable=True),
    sa.Column('last_name', sa.String(length=150), nullable=True),
    sa.Column('major', sa.String(length=150), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sgb_Student')
    # ### end Alembic commands ###
