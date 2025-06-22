"""Adjust Escala hierarchy for Strategy pattern

Revision ID: e26c95c996d8
Revises: 
Create Date: 2025-06-18 14:59:46.727215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e26c95c996d8'
down_revision = '000_create_especializacoes_medicos'
branch_labels = None
depends_on = None


def upgrade():
    # Criar tabela escala
    op.create_table(
        'escala',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('data_inicio', sa.Date, nullable=False),
        sa.Column('data_fim', sa.Date, nullable=False),
        sa.Column('tipo', sa.String(50), nullable=False),
        sa.Column('medico_id', sa.Integer, sa.ForeignKey(
            'medico.id'), nullable=False)
    )

    # Criar tabela escala_plantonista
    op.create_table(
        'escala_plantonista',
        sa.Column('id', sa.Integer, sa.ForeignKey(
            'escala.id'), primary_key=True),
        sa.Column('turno', sa.String(50), nullable=False)
    )

    # Criar tabela escala_sobreaviso
    op.create_table(
        'escala_sobreaviso',
        sa.Column('id', sa.Integer, sa.ForeignKey(
            'escala.id'), primary_key=True),
        sa.Column('especialidade_id', sa.Integer, sa.ForeignKey(
            'especializacao.id'), nullable=False)
    )


def downgrade():
    # Remover tabelas criadas
    op.drop_table('escala_sobreaviso')
    op.drop_table('escala_plantonista')
    op.drop_table('escala')
