"""
Factory para criação de objetos de relatório/exportação (PDF, CSV, etc).
Permite fácil extensão para novos formatos.
"""
class RelatorioFactory:
    @staticmethod
    def criar_relatorio(tipo, dados):
        if tipo == 'pdf':
            return RelatorioPDF(dados)
        elif tipo == 'csv':
            return RelatorioCSV(dados)
        else:
            raise ValueError(f"Tipo de relatório não suportado: {tipo}")

class RelatorioPDF:
    def __init__(self, dados):
        self.dados = dados
    def exportar(self):
        # Implementação real de exportação para PDF
        return f"PDF gerado com {len(self.dados)} registros"

class RelatorioCSV:
    def __init__(self, dados):
        self.dados = dados
    def exportar(self):
        # Implementação real de exportação para CSV
        return f"CSV gerado com {len(self.dados)} registros"

# Exemplo de uso:
# relatorio = RelatorioFactory.criar_relatorio('pdf', dados)
# resultado = relatorio.exportar()
