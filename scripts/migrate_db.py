"""
Script de migração de dados entre bancos (SQLite, PostgreSQL) para ambientes dev,
teste, produção.

Uso:
    python migrate_db.py --src-db <caminho_ou_url_origem> \
        --dst-db <caminho_ou_url_destino> [--tables tabela1,tabela2,...]

Exemplo:
    python migrate_db.py --src-db gem_dev.db --dst-db gem_prod.db \
        --tables medicos,especializacoes
"""
import argparse
import sys
import os
from sqlalchemy import create_engine, MetaData, Table


def parse_args():
    parser = argparse.ArgumentParser(
        description="Migração de dados entre bancos de dados."
    )
    parser.add_argument(
        '--src-db', required=True,
        help='Caminho ou URL do banco de origem (ex: gem_dev.db ou postgresql://...)'
    )
    parser.add_argument(
        '--dst-db', required=True,
        help='Caminho ou URL do banco de destino (ex: gem_prod.db ou postgresql://...)'
    )
    parser.add_argument(
        '--tables',
        help='Lista de tabelas a migrar, separadas por vírgula. Se omitido, migra todas.'
    )
    return parser.parse_args()


def get_engine(db_path_or_url):
    if db_path_or_url.startswith('sqlite:///') or db_path_or_url.startswith('postgresql://'):
        return create_engine(db_path_or_url)
    if db_path_or_url.endswith('.db'):
        return create_engine(f'sqlite:///{db_path_or_url}')
    return create_engine(db_path_or_url)


class TableMigrationStrategy:
    """Interface para estratégias de migração de tabelas."""
    def migrate(self, src_engine, dst_engine, table_name):
        raise NotImplementedError


class SQLiteTableMigrationStrategy(TableMigrationStrategy):
    def migrate(self, src_engine, dst_engine, table_name):
        src_meta = MetaData()
        dst_meta = MetaData()
        src_table = Table(table_name, src_meta, autoload_with=src_engine)
        dst_table = Table(table_name, dst_meta, autoload_with=dst_engine)
        print(f"[DEBUG] Origem: {src_engine.url}")
        print(f"[DEBUG] Destino: {dst_engine.url}")
        print(f"[DEBUG] Schema origem: {[c.name for c in src_table.columns]}")
        print(f"[DEBUG] Schema destino: {[c.name for c in dst_table.columns]}")
        with src_engine.begin() as src_conn, dst_engine.begin() as dst_conn:
            rows = list(src_conn.execute(src_table.select()))
            print(f"[DEBUG] Registros origem: {len(rows)}")
            if not rows:
                print(f"Tabela {table_name}: nada a migrar.")
                return
            dst_conn.execute(dst_table.delete())  # Limpa destino
            try:
                result = dst_conn.execute(dst_table.insert(), [dict(row._mapping) for row in rows])
                print(f"[DEBUG] Insert executado: {result.rowcount if hasattr(result, 'rowcount') else 'N/A'}")
            except Exception as exc:
                print(f"[ERRO] Falha ao inserir em {table_name}: {exc}")
                raise
            count = dst_conn.execute(dst_table.count()).scalar()
            print(f"Tabela {table_name}: {len(rows)} registros migrados. Total destino: {count}")


def get_strategy(src_engine, dst_engine):
    # Futuro: pode inspecionar engines para decidir a estratégia
    # Aqui, só SQLite
    return SQLiteTableMigrationStrategy()


def main():
    args = parse_args()
    print(f"Banco origem: {os.path.abspath(args.src_db)}")
    print(f"Banco destino: {os.path.abspath(args.dst_db)}")
    src_engine = get_engine(args.src_db)
    dst_engine = get_engine(args.dst_db)
    src_meta = MetaData()
    src_meta.reflect(bind=src_engine)
    tables = (
        args.tables.split(',') if args.tables else list(src_meta.tables.keys())
    )
    strategy = get_strategy(src_engine, dst_engine)
    for table in tables:
        if table not in src_meta.tables:
            print(
                f"Tabela {table} não encontrada no banco de origem.",
                file=sys.stderr
            )
            continue
        try:
            strategy.migrate(src_engine, dst_engine, table)
        except Exception as exc:
            print(
                f"Erro ao migrar tabela {table}: {exc}",
                file=sys.stderr
            )
    print("Migração concluída.")


if __name__ == "__main__":
    main()
