"""
Utilitários para upload, validação e otimização de imagens.
"""
import os
import uuid
from PIL import Image
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
MAX_IMAGE_SIZE_MB = 2
IMAGE_FOLDER = os.path.join("static", "assets", "images")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_image(file_storage):
    if not allowed_file(file_storage.filename):
        raise ValueError("Tipo de arquivo não permitido.")
    file_storage.seek(0, os.SEEK_END)
    size_mb = file_storage.tell() / (1024 * 1024)
    if size_mb > MAX_IMAGE_SIZE_MB:
        raise ValueError("Imagem excede o tamanho máximo permitido.")
    file_storage.seek(0)
    try:
        img = Image.open(file_storage)
        img.verify()
        # Revalida magic number (assinatura real do arquivo)
        if img.format.lower() not in ALLOWED_EXTENSIONS:
            raise ValueError("Formato de imagem não permitido.")
    except Exception:
        raise ValueError("Arquivo não é uma imagem válida.")
    file_storage.seek(0)


def save_image(file_storage):
    validate_image(file_storage)
    ext = file_storage.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filename = secure_filename(filename)
    path = os.path.join(IMAGE_FOLDER, filename)
    os.makedirs(IMAGE_FOLDER, exist_ok=True)
    file_storage.seek(0)
    img = Image.open(file_storage)
    img = img.convert("RGB")
    # Otimização: redimensiona se maior que 1200x1200px
    max_dim = 1200
    if img.width > max_dim or img.height > max_dim:
        ratio = min(max_dim / img.width, max_dim / img.height)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)
    img.save(path, optimize=True, quality=80)
    return os.path.relpath(path, start="static")

# Uso: caminho_relativo = save_image(request.files['imagem'])
