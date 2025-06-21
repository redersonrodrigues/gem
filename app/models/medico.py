from sqlalchemy import Column, Integer, String, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum
from .base import Base


class StatusMedicoEnum(enum.Enum):
    ATIVO = 'ativo'
    INATIVO = 'inativo'
    AFASTADO = 'afastado'

    def __str__(self):
        return self.value


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
        ),
        nullable=False,
    )
    version = Column(Integer, nullable=False, default=1)
    __mapper_args__ = {"version_id_col": version}

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

    def __init__(self, nome, especializacao_id, nome_pj=None, status=StatusMedicoEnum.ATIVO.value):
        self.nome = nome
        self.nome_pj = nome_pj
        self.especializacao_id = especializacao_id
        # Garante que status sempre seja string
        if isinstance(status, StatusMedicoEnum):
            self.status = status.value
        else:
            self.status = str(status)

    def __repr__(self):
        """
        Retorna uma representação legível do médico para debug/log.
        """
        return f"<Medico(nome={self.nome}, status={self.status})>"

    def to_dict(self):
        """
        Serializa o médico para dicionário, convertendo status para string (valor do Enum).
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'nome_pj': self.nome_pj,
            'especializacao_id': self.especializacao_id,
            'status': self.status.value if hasattr(self.status, 'value') else str(self.status)
        }
