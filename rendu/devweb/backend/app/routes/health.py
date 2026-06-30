"""
Routes pour l'état de l'application
"""
from flask import Blueprint, jsonify
from app.services.ollama_service import OllamaService
from flask import current_app

health_bp = Blueprint('health', __name__, url_prefix='/api')

@health_bp.route('/health', methods=['GET'])
def health():
    """Vérifier l'état de santé de l'application"""
    ollama_healthy = OllamaService.check_health()
    
    return jsonify({
        'status': 'healthy' if ollama_healthy else 'degraded',
        'ollama': 'connected' if ollama_healthy else 'disconnected',
        'models': OllamaService.list_models() if ollama_healthy else []
    }), 200 if ollama_healthy else 503

@health_bp.route('/status', methods=['GET'])
def status():
    """Statut complet du serveur"""
    ollama_healthy = OllamaService.check_health()
    
    return jsonify({
        'service': 'Financial Assistant API',
        'version': '1.0.0',
        'ollama_host': current_app.config['OLLAMA_HOST'],
        'ollama_model': current_app.config['OLLAMA_MODEL'],
        'ollama_connected': ollama_healthy
    }), 200
