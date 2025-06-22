import json
from sqlalchemy import event, inspect
from sqlalchemy.orm import Session
from datetime import datetime, date
from .medico import Medico
from .especializacao import Especializacao
from .escala_plantonista import EscalaPlantonista
from .escala_sobreaviso import EscalaSobreaviso
from .audit_log import AuditLog
from .historico_versao import HistoricoVersao

def serializar_valores(dados):
    import enum
    def serializar(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, enum.Enum):
            return obj.value
        return obj
    return {k: serializar(v) for k, v in dados.items()}

# Função para obter usuário logado (integração real com sistema de autenticação)
def obter_usuario_logado():
    """
    Retorna o nome do usuário atualmente autenticado no sistema.
    - Flask: use flask_login.current_user ou session['user']
    - PyQt: obtenha do contexto da aplicação ou singleton de sessão
    - CLI/testes: pode retornar 'admin' ou usuário de teste
    Adapte conforme o backend real.
    """
    # Exemplo para Flask:
    # from flask_login import current_user
    # return current_user.username if current_user.is_authenticated else 'anon'
    # Exemplo para PyQt:
    # return SessaoUsuario.get_usuario_atual()
    return 'admin'  # TODO: integrar com autenticação real

def registrar_versao(session, target, operacao):
    """
    Salva uma nova versão do registro no histórico de versões.
    """
    from sqlalchemy import inspect
    import json
    tabela = target.__tablename__
    registro_id = getattr(target, 'id', None)
    versao = getattr(target, 'version', 1) if hasattr(target, 'version') else 1
    usuario = obter_usuario_logado()
    dados = serializar_valores({c.name: getattr(target, c.name) for c in target.__table__.columns})
    historico = HistoricoVersao(
        tabela=tabela,
        registro_id=registro_id,
        versao=versao,
        usuario=usuario,
        dados=json.dumps(dados, ensure_ascii=False)
    )
    session.add(historico)

def registrar_auditoria(mapper, connection, target):
    session = Session.object_session(target)
    usuario = obter_usuario_logado()
    tabela = target.__tablename__
    registro_id = getattr(target, 'id', None)
    dados_novos = serializar_valores({c.name: getattr(target, c.name) for c in target.__table__.columns})
    data_hora = datetime.now().isoformat(sep=' ', timespec='seconds')
    # INSERT
    audit = AuditLog(
        usuario=usuario,
        data_hora=data_hora,
        operacao='INSERT',
        tabela=tabela,
        registro_id=registro_id,
        dados_anteriores=None,
        dados_novos=json.dumps(dados_novos, ensure_ascii=False)
    )
    session.add(audit)
    # Registrar versão também no INSERT
    if session:
        registrar_versao(session, target, 'INSERT')

def registrar_auditoria_update(mapper, connection, target):
    session = Session.object_session(target)
    usuario = obter_usuario_logado()
    tabela = target.__tablename__
    registro_id = getattr(target, 'id', None)
    # Usar inspection do SQLAlchemy para acessar histórico de alterações
    state = inspect(target)
    dados_anteriores = {}
    for attr in target.__table__.columns:
        hist = state.attrs[attr.name].history
        if hist.has_changes():
            dados_anteriores[attr.name] = hist.deleted[0] if hist.deleted else None
    dados_anteriores = serializar_valores(dados_anteriores)
    dados_novos = serializar_valores({c.name: getattr(target, c.name) for c in target.__table__.columns})
    data_hora = datetime.now().isoformat(sep=' ', timespec='seconds')
    audit = AuditLog(
        usuario=usuario,
        data_hora=data_hora,
        operacao='UPDATE',
        tabela=tabela,
        registro_id=registro_id,
        dados_anteriores=json.dumps(dados_anteriores, ensure_ascii=False),
        dados_novos=json.dumps(dados_novos, ensure_ascii=False)
    )
    session.add(audit)
    # Registrar versão sempre que houver alteração
    if session:
        registrar_versao(session, target, 'UPDATE')

def registrar_auditoria_delete(mapper, connection, target):
    session = Session.object_session(target)
    usuario = obter_usuario_logado()
    tabela = target.__tablename__
    registro_id = getattr(target, 'id', None)
    dados_anteriores = serializar_valores({c.name: getattr(target, c.name) for c in target.__table__.columns})
    data_hora = datetime.now().isoformat(sep=' ', timespec='seconds')
    audit = AuditLog(
        usuario=usuario,
        data_hora=data_hora,
        operacao='DELETE',
        tabela=tabela,
        registro_id=registro_id,
        dados_anteriores=json.dumps(dados_anteriores, ensure_ascii=False),
        dados_novos=None
    )
    session.add(audit)
    # Registrar versão no histórico ao deletar registro
    if session:
        registrar_versao(session, target, 'DELETE')

# Registrar listeners para os modelos Medico, Especializacao, EscalaPlantonista, EscalaSobreaviso
for modelo in [Medico, Especializacao, EscalaPlantonista, EscalaSobreaviso]:
    for event_name, fn in [
        ('after_insert', registrar_auditoria),
        ('after_update', registrar_auditoria_update),
        ('after_delete', registrar_auditoria_delete),
    ]:
        event.listen(modelo, event_name, fn)
