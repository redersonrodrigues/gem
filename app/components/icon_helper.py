"""
Helper para uso de ícones FontAwesome locais na interface PyQt5
"""
import os
from PyQt5.QtGui import QIcon

ICON_MAP = {
    "add": "fa-plus.png",
    "edit": "fa-edit.png",
    "delete": "fa-trash.png",
    "search": "fa-search.png",
    "user": "fa-user-md.png",
    "calendar": "fa-calendar-alt.png",
    "alert": "fa-exclamation-triangle.png",
    "help": "fa-question-circle.png",
    # Adicione mais mapeamentos conforme necessário
}

ICON_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "static", "assets", "icons")

def get_icon(name: str) -> QIcon:
    filename = ICON_MAP.get(name)
    if not filename:
        return QIcon()
    path = os.path.join(ICON_PATH, filename)
    return QIcon(path)
