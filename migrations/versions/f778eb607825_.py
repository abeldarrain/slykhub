"""empty message

Revision ID: f778eb607825
Revises: e2dc5f974b34
Create Date: 2023-04-10 13:30:28.641071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f778eb607825'
down_revision = 'e2dc5f974b34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('active_slyk_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'slyk', ['active_slyk_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('active_slyk_id')

    # ### end Alembic commands ###
