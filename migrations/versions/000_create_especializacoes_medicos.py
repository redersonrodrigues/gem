"""cria tabelas especializacoes e medicos

Revision ID: 000_create_especializacoes_medicos
Revises: 
Create Date: 2025-06-21 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# Revisão e dependência
revision = '000_create_especializacoes_medicos'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'especializacoes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nome', sa.String, unique=True, nullable=False),
        sa.Column('version', sa.Integer, nullable=False, server_default='1'),
    )
    op.create_table(
        'medicos',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nome', sa.String, nullable=False),
        sa.Column('nome_pj', sa.String),
        sa.Column('especializacao_id', sa.Integer, sa.ForeignKey('especializacoes.id'), nullable=False),
        sa.Column('status', sa.String, nullable=False),
        sa.Column('version', sa.Integer, nullable=False, server_default='1'),
        sa.UniqueConstraint('nome', 'especializacao_id', name='uix_nome_especializacao'),
    )

def downgrade():
    op.drop_table('medicos')
    op.drop_table('especializacoes')
