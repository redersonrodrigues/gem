"""cria tabela usuarios

Revision ID: 001_create_usuario
Revises: 
Create Date: 2025-06-21 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# Revisão e dependência
revision = '001_create_usuario'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nome', sa.String(100), nullable=False),
        sa.Column('login', sa.String(50), unique=True, nullable=False),
        sa.Column('senha_hash', sa.String(128), nullable=False),
        sa.Column('perfil', sa.String(20), nullable=False, server_default='usuario'),
        sa.Column('status', sa.Boolean, server_default=sa.sql.expression.true()),
        sa.Column('data_criacao', sa.DateTime, nullable=False),
    )

def downgrade():
    op.drop_table('usuarios')
