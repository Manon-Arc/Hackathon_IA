"""
Routes pour les endpoints de chat
"""
from flask import Blueprint, request, jsonify
from app.services.chat_service import ChatService
from app.services.ollama_service import OllamaService
from app.utils.decorators import handle_errors, require_json
import uuid

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

@chat_bp.route('/message', methods=['POST'])
@require_json
@handle_errors
def send_message():
    """
    Envoyer un message et recevoir une réponse
    
    Payload:
    {
        "session_id": "uuid",
        "message": "votre question"
    }
    """
    data = request.get_json()
    
    # Validation
    if not data.get('message'):
        return jsonify({'success': False, 'error': 'Message required'}), 400
    
    session_id = data.get('session_id', str(uuid.uuid4()))
    user_message = data.get('message').strip()
    
    # Vérifier la connexion à Ollama
    if not OllamaService.check_health():
        return jsonify({
            'success': False,
            'error': 'Serveur Ollama indisponible'
        }), 503
    
    # Traiter le message
    result = ChatService.process_message(session_id, user_message)
    
    if result['success']:
        return jsonify({
            'success': True,
            'session_id': session_id,
            'user_message': result['user_message'],
            'bot_response': result['bot_response']
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500

@chat_bp.route('/history/<session_id>', methods=['GET'])
@handle_errors
def get_history(session_id):
    """Récupérer l'historique d'une session"""
    history = ChatService.get_history(session_id)
    return jsonify({
        'success': True,
        'session_id': session_id,
        'messages': history
    }), 200

@chat_bp.route('/sessions', methods=['GET'])
@handle_errors
def get_sessions():
    """Lister toutes les sessions"""
    sessions = ChatService.get_all_sessions()
    return jsonify({
        'success': True,
        'sessions': sessions,
        'count': len(sessions)
    }), 200

@chat_bp.route('/session/<session_id>', methods=['DELETE'])
@handle_errors
def delete_session(session_id):
    """Supprimer une session"""
    if ChatService.delete_session(session_id):
        return jsonify({
            'success': True,
            'message': f'Session {session_id} deleted'
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': 'Session not found'
        }), 404

@chat_bp.route('/clear/<session_id>', methods=['POST'])
@handle_errors
def clear_session(session_id):
    """Vider l'historique d'une session (garder la session)"""
    if ChatService.delete_session(session_id):
        ChatService.create_session(session_id)
        return jsonify({
            'success': True,
            'message': 'Session cleared'
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': 'Session not found'
        }), 404
