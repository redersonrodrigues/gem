"""cria tabela audit_log

Revision ID: 002_create_audit_log
Revises: 001_create_usuario
Create Date: 2025-06-21 15:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# Revisão e dependência
revision = '002_create_audit_log'
down_revision = '001_create_usuario'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'audit_log',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('usuario', sa.String),
        sa.Column('data_hora', sa.String),
        sa.Column('operacao', sa.String),
        sa.Column('tabela', sa.String),
        sa.Column('registro_id', sa.Integer),
        sa.Column('dados_anteriores', sa.Text),
        sa.Column('dados_novos', sa.Text),
    )

def downgrade():
    op.drop_table('audit_log')
