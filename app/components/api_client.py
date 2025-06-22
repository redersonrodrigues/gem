"""
Cliente desacoplado para integração com APIs externas
"""
import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data=None, json=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.post(url, data=data, json=json)
        response.raise_for_status()
        return response.json()
