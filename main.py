from lib.core.application_loader import ApplicationLoader

if __name__ == "__main__":
    print("Iniciando aplicação GEM...")
    try:
        ApplicationLoader().run()
    except Exception as e:
        print(f"Erro ao iniciar a aplicação: {e}")
    print("Aplicação finalizada.")
