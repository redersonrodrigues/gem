import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), '../../logs/ui_actions.log')
LOG_PATH = os.path.abspath(LOG_PATH)

def log_action(user, action, entity, entity_id=None, details=None, result='sucesso'):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = (
        f"[{timestamp}] user={user} action={action} entity={entity} id={entity_id} "
        f"result={result} details={details}\n"
    )
    try:
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(entry)
    except Exception as e:
        print(f"Erro ao registrar log de ação: {e}")
