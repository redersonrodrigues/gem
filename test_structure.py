# Script de teste para verificar a funcionalidade da aplicação reestruturada
import sys
import os

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.abspath('.'))

def test_imports():
    """Testa se todos os imports estão funcionando"""
    print("Testando imports...")
    
    try:
        # Testar imports dos modelos
        from gem.models import Hospital, Medico, Especializacao
        print("✓ Modelos importados com sucesso")
        
        # Testar imports dos repositórios
        from gem.repositories import HospitalRepository, MedicoRepository, EspecializacaoRepository
        print("✓ Repositórios importados com sucesso")
        
        # Testar imports dos serviços
        from gem.services import HospitalService, MedicoService, EspecializacaoService
        print("✓ Serviços importados com sucesso")
        
        # Testar imports dos controladores
        from gem.controllers import HospitalController, MedicoController
        print("✓ Controladores importados com sucesso")
        
        # Testar import da aplicação
        from gem.app import create_app
        print("✓ Aplicação importada com sucesso")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro nos imports: {e}")
        return False

def test_controllers():
    """Testa básicamente os controladores"""
    print("\nTestando controladores...")
    
    try:
        from gem.controllers import HospitalController, MedicoController
        
        # Testar instanciação dos controladores
        hospital_controller = HospitalController()
        medico_controller = MedicoController()
        
        print("✓ Controladores instanciados com sucesso")
        
        # Testar validação de ID
        try:
            hospital_controller.validate_id("abc")
            print("✗ Validação de ID falhou")
            return False
        except ValueError:
            print("✓ Validação de ID funcionando")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro nos controladores: {e}")
        return False

def test_services():
    """Testa básicamente os serviços"""
    print("\nTestando serviços...")
    
    try:
        from gem.services import HospitalService, MedicoService, EspecializacaoService
        
        # Testar instanciação dos serviços
        hospital_service = HospitalService()
        medico_service = MedicoService()
        especializacao_service = EspecializacaoService()
        
        print("✓ Serviços instanciados com sucesso")
        
        # Testar validação básica
        try:
            hospital_service.criar_hospital("", "")
            print("✗ Validação de serviço falhou")
            return False
        except ValueError:
            print("✓ Validação de serviço funcionando")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro nos serviços: {e}")
        return False

def main():
    """Função principal de teste"""
    print("=== TESTE DA APLICAÇÃO REESTRUTURADA ===\n")
    
    success = True
    
    success &= test_imports()
    success &= test_controllers()
    success &= test_services()
    
    print("\n=== RESULTADO DOS TESTES ===")
    if success:
        print("✓ Todos os testes passaram! A reestruturação foi bem-sucedida.")
    else:
        print("✗ Alguns testes falharam. Verifique os imports e dependências.")
    
    return success

if __name__ == "__main__":
    main()