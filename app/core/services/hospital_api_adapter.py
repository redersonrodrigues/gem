"""
Adapter para integração desacoplada com sistemas hospitalares via API REST.
Permite trocar o backend externo sem alterar a lógica de negócio interna.
"""
import requests

class HospitalApiAdapter:
    def __init__(self, base_url, token=None):
        self.base_url = base_url
        self.token = token

    def get_medicos(self):
        url = f"{self.base_url}/medicos"
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def post_escala(self, escala_dict):
        url = f"{self.base_url}/escalas"
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        response = requests.post(url, json=escala_dict, headers=headers)
        response.raise_for_status()
        return response.json()

# Exemplo de uso:
# adapter = HospitalApiAdapter("https://api.hospital.com", token="seutoken")
# medicos = adapter.get_medicos()
# resultado = adapter.post_escala({"data": "2025-06-22", ...})
