"""
Bridge para integração desacoplada entre interface PyQt5 e backend Flask/local
"""
import requests

class BackendBridge:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')

    def get_medicos(self):
        url = f"{self.base_url}/api/medicos"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_especializacoes(self):
        url = f"{self.base_url}/api/especializacoes"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_escalas(self):
        url = f"{self.base_url}/api/escalas"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_medicos_by_especializacao(self, especializacao_id):
        # Mock para desenvolvimento: sempre retorna lista vazia
        return []

    def get_escalas_by_medico(self, medico_id):
        # TODO: Implementar busca real de escalas por médico se necessário
        return []

    # Métodos POST/PUT/DELETE podem ser adicionados conforme necessário
    def update_medico(self, medico_id, data, versao):
        url = f"{self.base_url}/api/medicos/{medico_id}"
        payload = data.copy()
        payload['versao'] = versao
        response = requests.put(url, json=payload)
        if response.status_code == 409:
            raise Exception("Conflito de concorrência: registro foi alterado por outro usuário.")
        if response.status_code == 400:
            raise Exception(response.json().get('detail', 'Erro de validação.'))
        if response.status_code == 500:
            raise Exception("Erro interno no servidor. Operação revertida.")
        response.raise_for_status()
        return response.json()

    def delete_medico(self, medico_id, versao):
        url = f"{self.base_url}/api/medicos/{medico_id}"
        response = requests.delete(url, json={"versao": versao})
        if response.status_code == 409:
            raise Exception("Conflito de concorrência: registro foi alterado por outro usuário.")
        if response.status_code == 400:
            raise Exception(response.json().get('detail', 'Erro de validação.'))
        if response.status_code == 500:
            raise Exception("Erro interno no servidor. Operação revertida.")
        response.raise_for_status()
        return response.json()

    # Repetir padrão para especializações e escalas conforme necessário
