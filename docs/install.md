# Guia de instalação e setup

Este documento irá orientar sobre como instalar e configurar o ambiente do projeto GEM.

## Pré-requisitos

- Python 3.8+
- pip
- (Opcional) DBeaver ou DB Browser SQLite

## Passos

1. Clone o repositório:
   ```sh
   git clone https://github.com/redersonrodrigues/gem.git
   ```
2. Crie e ative o ambiente virtual:
   ```sh
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
4. Configure variáveis de ambiente, se necessário, no arquivo `.env`.
5. Execute a aplicação:
   ```sh
   python main.py
   ```

Consulte a documentação técnica para detalhes avançados.
