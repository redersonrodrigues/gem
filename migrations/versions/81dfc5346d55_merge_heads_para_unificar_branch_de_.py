"""merge heads para unificar branch de migrations

Revision ID: 81dfc5346d55
Revises: 002_create_audit_log, 85c8f95a0c5d
Create Date: 2025-06-21 21:52:29.625025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81dfc5346d55'
down_revision = ('002_create_audit_log', '85c8f95a0c5d')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
