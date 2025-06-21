"""merge heads

Revision ID: 85c8f95a0c5d
Revises: 001_create_usuario, e26c95c996d8
Create Date: 2025-06-21 14:23:15.308731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85c8f95a0c5d'
down_revision = ('001_create_usuario', 'e26c95c996d8')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
