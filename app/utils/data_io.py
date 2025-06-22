import csv
import json
import os
from PyQt5.QtWidgets import QFileDialog

def export_to_csv(parent, headers, data, default_name="export.csv"):
    path, _ = QFileDialog.getSaveFileName(parent, "Exportar CSV", default_name, "CSV Files (*.csv)")
    if not path:
        return False
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)
    return True

def import_from_csv(parent):
    path, _ = QFileDialog.getOpenFileName(parent, "Importar CSV", "", "CSV Files (*.csv)")
    if not path:
        return None
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    return rows

def export_to_json(parent, data, default_name="export.json"):
    path, _ = QFileDialog.getSaveFileName(parent, "Exportar JSON", default_name, "JSON Files (*.json)")
    if not path:
        return False
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True

def import_from_json(parent):
    path, _ = QFileDialog.getOpenFileName(parent, "Importar JSON", "", "JSON Files (*.json)")
    if not path:
        return None
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
