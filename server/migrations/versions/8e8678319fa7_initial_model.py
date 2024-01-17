"""initial model

Revision ID: 8e8678319fa7
Revises: 657a7f5e92a7
Create Date: 2024-01-17 10:57:37.783824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e8678319fa7'
down_revision = '657a7f5e92a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('signups', sa.Column('camper_id', sa.Integer(), nullable=False))
    op.add_column('signups', sa.Column('activity_id', sa.Integer(), nullable=False))
    op.create_foreign_key(op.f('fk_signups_camper_id_campers'), 'signups', 'campers', ['camper_id'], ['id'])
    op.create_foreign_key(op.f('fk_signups_activity_id_activities'), 'signups', 'activities', ['activity_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_signups_activity_id_activities'), 'signups', type_='foreignkey')
    op.drop_constraint(op.f('fk_signups_camper_id_campers'), 'signups', type_='foreignkey')
    op.drop_column('signups', 'activity_id')
    op.drop_column('signups', 'camper_id')
    # ### end Alembic commands ###
