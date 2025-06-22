"""
Temas e estilos para a interface PyQt5
"""
LIGHT_THEME = """
QWidget {
    background: #f5f5f5;
    color: #222;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}
QPushButton {
    background: #1976d2;
    color: white;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
}
QPushButton:hover {
    background: #1565c0;
}
QTableWidget {
    background: #fff;
    border: 1px solid #ccc;
    border-radius: 4px;
}
QHeaderView::section {
    background: #1976d2;
    color: white;
    font-weight: bold;
}
QLineEdit {
    background: #fff;
    border: 1px solid #bbb;
    border-radius: 4px;
    padding: 6px;
}
"""

DARK_THEME = """
QWidget {
    background: #23272e;
    color: #f5f5f5;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}
QPushButton {
    background: #1976d2;
    color: white;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
}
QPushButton:hover {
    background: #1565c0;
}
QTableWidget {
    background: #2c313a;
    border: 1px solid #444;
    border-radius: 4px;
}
QHeaderView::section {
    background: #1976d2;
    color: white;
    font-weight: bold;
}
QLineEdit {
    background: #2c313a;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 6px;
}
"""
