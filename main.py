# Ponto de entrada principal da aplicação GEM
# Sistema de Gestão de Escalas Médicas

from gem.app import create_app, populate_initial_data

def main():
    """Função principal da aplicação"""
    print("Iniciando Sistema GEM - Gestão de Escalas Médicas")
    
    # Criar aplicação Flask
    app = create_app()
    
    # Popular dados iniciais se necessário
    with app.app_context():
        try:
            populate_initial_data()
        except Exception as e:
            print(f"Aviso: Erro ao popular dados iniciais: {e}")
    
    # Iniciar aplicação
    print("Aplicação iniciada com sucesso!")
    print("Acesse: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()