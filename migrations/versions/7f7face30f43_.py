"""empty message

Revision ID: 7f7face30f43
Revises: f778eb607825
Create Date: 2023-04-10 13:31:24.332135

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f7face30f43'
down_revision = 'f778eb607825'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('user_active_slyk_id_fkey', type_='foreignkey')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_foreign_key('user_active_slyk_id_fkey', 'slyk', ['active_slyk_id'], ['id'])

    # ### end Alembic commands ###
