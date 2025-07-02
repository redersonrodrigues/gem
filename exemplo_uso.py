# Exemplo de uso da nova estrutura MVC
# Este script demonstra como usar os serviços e controladores

import sys
import os

# Adicionar o diretório do projeto ao path (apenas para exemplo)
sys.path.insert(0, os.path.abspath('.'))

def exemplo_uso_servicos():
    """Demonstra o uso da camada de serviços"""
    print("=== EXEMPLO: USO DOS SERVIÇOS ===\n")
    
    # Este código funcionará quando as dependências estiverem instaladas
    exemplo_codigo = '''
    from gem.services import HospitalService, MedicoService, EspecializacaoService
    
    # Instanciar serviços
    hospital_service = HospitalService()
    medico_service = MedicoService()
    especializacao_service = EspecializacaoService()
    
    # Criar hospital
    try:
        hospital = hospital_service.criar_hospital("Hospital São José", "Rua das Flores, 123")
        print(f"Hospital criado: ID {hospital.id} - {hospital.nome}")
    except ValueError as e:
        print(f"Erro ao criar hospital: {e}")
    
    # Listar hospitais
    hospitais = hospital_service.listar_hospitais()
    print(f"Total de hospitais: {len(hospitais)}")
    
    # Criar médico
    try:
        medico = medico_service.criar_medico("Dr. João Silva")
        print(f"Médico criado: ID {medico.id} - {medico.nome}")
    except ValueError as e:
        print(f"Erro ao criar médico: {e}")
    
    # Popular especializações iniciais
    especializacao_service.popular_especializacoes_iniciais()
    especializacoes = especializacao_service.listar_especializacoes()
    print(f"Especializações disponíveis: {[e.nome for e in especializacoes]}")
    '''
    
    print("Código de exemplo (executar quando dependências estiverem instaladas):")
    print(exemplo_codigo)

def exemplo_uso_controladores():
    """Demonstra o uso da camada de controladores"""
    print("\n=== EXEMPLO: USO DOS CONTROLADORES ===\n")
    
    exemplo_codigo = '''
    from gem.controllers import HospitalController, MedicoController
    
    # Instanciar controladores
    hospital_controller = HospitalController()
    medico_controller = MedicoController()
    
    # Criar hospital via controlador
    resposta = hospital_controller.criar_hospital("Hospital Central", "Av. Principal, 456")
    
    if resposta['success']:
        print(f"Sucesso: {resposta['message']}")
        print(f"Dados: {resposta['data']}")
    else:
        print(f"Erro: {resposta['error']}")
    
    # Listar hospitais
    resposta = hospital_controller.listar_hospitais()
    if resposta['success']:
        for hospital in resposta['data']:
            print(f"Hospital: {hospital['nome']} - {hospital['endereco']}")
    
    # Buscar hospital por ID
    resposta = hospital_controller.buscar_hospital(1)
    if resposta['success'] and resposta['data']:
        hospital = resposta['data']
        print(f"Hospital encontrado: {hospital['nome']}")
    else:
        print("Hospital não encontrado")
    '''
    
    print("Código de exemplo (executar quando dependências estiverem instaladas):")
    print(exemplo_codigo)

def exemplo_estrutura_resposta():
    """Demonstra a estrutura padronizada de resposta"""
    print("\n=== ESTRUTURA PADRONIZADA DE RESPOSTA ===\n")
    
    print("Os controladores retornam sempre o mesmo formato:")
    print("""
    {
        'success': bool,      # True se operação bem-sucedida
        'data': object,       # Dados retornados (None se erro)
        'message': str,       # Mensagem de sucesso (None se erro)
        'error': str          # Mensagem de erro (None se sucesso)
    }
    """)
    
    print("Exemplos de resposta:")
    print("\nSucesso:")
    print("""
    {
        'success': True,
        'data': {'id': 1, 'nome': 'Hospital X', 'endereco': 'Rua Y'},
        'message': 'Hospital criado com sucesso',
        'error': None
    }
    """)
    
    print("Erro:")
    print("""
    {
        'success': False,
        'data': None,
        'message': None,
        'error': 'Nome do hospital é obrigatório'
    }
    """)

def exemplo_arquitetura():
    """Explica a arquitetura em camadas"""
    print("\n=== ARQUITETURA EM CAMADAS ===\n")
    
    print("Interface/UI → Controllers → Services → Repositories → Database")
    print()
    print("1. MODELS (gem/models/): Definição das entidades")
    print("   - Hospital, Médico, Especialização")
    print("   - Relacionamentos e validações básicas")
    print()
    print("2. REPOSITORIES (gem/repositories/): Acesso aos dados")
    print("   - CRUD básico para cada entidade")
    print("   - Queries específicas")
    print("   - Abstração do banco de dados")
    print()
    print("3. SERVICES (gem/services/): Lógica de negócio")
    print("   - Validações complexas")
    print("   - Regras de negócio")
    print("   - Coordenação entre repositórios")
    print()
    print("4. CONTROLLERS (gem/controllers/): Interface de apresentação")
    print("   - Validação de entrada")
    print("   - Formatação de resposta")
    print("   - Tratamento de erros")
    print()
    print("5. VIEWS (gem/views/): Interface de usuário")
    print("   - PyQt5 (futuro)")
    print("   - Templates Flask (opcional)")

def exemplo_instalacao():
    """Instruções de instalação"""
    print("\n=== INSTALAÇÃO E EXECUÇÃO ===\n")
    
    print("1. Instalar dependências:")
    print("   pip install -r requirements.txt")
    print()
    print("2. Executar aplicação:")
    print("   python main.py")
    print()
    print("3. Testar estrutura:")
    print("   python test_structure.py")
    print()
    print("4. Executar migrações:")
    print("   cd gem/alembic")
    print("   alembic upgrade head")

def main():
    """Função principal de demonstração"""
    print("DEMONSTRAÇÃO DA NOVA ESTRUTURA MVC - GEM")
    print("=" * 50)
    
    exemplo_uso_servicos()
    exemplo_uso_controladores() 
    exemplo_estrutura_resposta()
    exemplo_arquitetura()
    exemplo_instalacao()
    
    print("\n" + "=" * 50)
    print("Para mais informações, consulte:")
    print("- README.md: Documentação geral")
    print("- ROL_DE_TAREFAS.md: Roteiro de desenvolvimento")
    print("- gem/docs/MIGRATION_GUIDE.md: Guia de migração")

if __name__ == "__main__":
    main()