import pytest
from PyQt5.QtWidgets import QApplication
from app.views.medicos_view import MedicosView

@pytest.fixture(scope="module")
def app():
    import sys
    app = QApplication.instance() or QApplication(sys.argv)
    yield app

@pytest.fixture
def view(app):
    return MedicosView()

def test_campos_existentes(view):
    assert view.search_input is not None
    assert view.table is not None

def test_botao_adicionar(view):
    botoes = [b for b in view.findChildren(type(view.search_input.parent().findChild(type(view.search_input)))) if b.text().startswith("Adicionar")]
    assert botoes

def test_validacao_campo_obrigatorio(view, qtbot):
    view.search_input.setText("")
    view.adicionar_medico()
    assert view.search_input.toolTip() != ""
