from sqlalchemy import Column, Integer, String, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum
from .base import Base


class StatusMedicoEnum(enum.Enum):
    ATIVO = 'ativo'
    INATIVO = 'inativo'


class Medico(Base):
    """
    Modelo ORM para médicos.

    Representa um médico do hospital, incluindo:
    - nome completo
    - nome da pessoa jurídica (opcional)
    - especialização (chave estrangeira para Especializacao)
    - status de atividade ('ativo' ou 'inativo')
    """
    __tablename__ = 'medicos'
    __table_args__ = (
        UniqueConstraint('nome', 'especializacao_id', name='uix_nome_especializacao'),
    )
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)  # Nome completo do médico
    nome_pj = Column(String)  # Nome da pessoa jurídica (opcional)
    especializacao_id = Column(
        Integer, ForeignKey('especializacoes.id'), nullable=False
    )  # FK para especialização
    status: Mapped[str] = mapped_column(
        Enum(
            StatusMedicoEnum,
            name="status_medico_enum",
            values_callable=lambda x: [e.value for e in x],
            native_enum=False
        ),
        nullable=False,
        default=StatusMedicoEnum.ATIVO.value
    )  # Status do médico: 'ativo' ou 'inativo', restrito por Enum

    especializacao = relationship(
        'Especializacao', back_populates='medicos'
    )  # Relação ORM
    escalas_plantonista1 = relationship(
        'EscalaPlantonista', foreign_keys='EscalaPlantonista.medico1_id', back_populates='medico1'
    )  # Relação com EscalaPlantonista (médico 1)
    escalas_plantonista2 = relationship(
        'EscalaPlantonista', foreign_keys='EscalaPlantonista.medico2_id', back_populates='medico2'
    )  # Relação com EscalaPlantonista (médico 2)
    escalas_sobreaviso = relationship(
        'EscalaSobreaviso', foreign_keys='EscalaSobreaviso.medico1_id', back_populates='medico1'
    )  # Relação com EscalaSobreaviso

    def __repr__(self):
        """
        Retorna uma representação legível do médico para debug/log.
        """
        return f"<Medico(nome={self.nome}, status={self.status})>"
