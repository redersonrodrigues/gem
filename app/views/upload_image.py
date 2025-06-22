import os
from flask import Blueprint, request, jsonify
from app.utils import image_utils
import logging

bp = Blueprint('upload_image', __name__)

@bp.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        logging.warning('Nenhum arquivo enviado no campo image.')
        return jsonify({'error': 'Nenhum arquivo enviado.'}), 400
    file = request.files['image']
    if file.filename == '':
        logging.warning('Nome de arquivo vazio.')
        return jsonify({'error': 'Nome de arquivo vazio.'}), 400
    try:
        relative_path = image_utils.save_image(file)
    except ValueError as e:
        logging.warning(f'Erro de validação: {e}')
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logging.error(f'Erro inesperado: {e}')
        return jsonify({'error': 'Erro ao processar imagem.'}), 500
    return jsonify({'success': True, 'image_path': relative_path.replace('\\', '/')})
