import argparse
import logging
import os
from app.utils.maintenance import check_integrity, vacuum, orphan_cleanup

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Rotinas de manutenção do banco de dados.")
    parser.add_argument('--db-path', required=True, help='Caminho do banco SQLite')
    parser.add_argument('--integrity', action='store_true', help='Verifica integridade do banco')
    parser.add_argument('--vacuum', action='store_true', help='Executa VACUUM')
    parser.add_argument('--cleanup', action='store_true', help='Remove registros órfãos')
    args = parser.parse_args()

    db_path = args.db_path
    if not os.path.exists(db_path):
        logging.error(f"Banco não encontrado: {db_path}")
        return
    if args.integrity:
        ok = check_integrity(db_path)
        if ok:
            print("Banco íntegro.")
        else:
            print("Problemas de integridade detectados!")
    if args.vacuum:
        vacuum(db_path)
        print("VACUUM executado.")
    if args.cleanup:
        orphan_cleanup(db_path)
        print("Limpeza de registros órfãos executada.")

if __name__ == "__main__":
    main()
