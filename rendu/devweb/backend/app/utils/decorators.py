"""
Décorateurs utilitaires
"""
from functools import wraps
from flask import jsonify, current_app

def handle_errors(f):
    """Décorateur pour gérer les erreurs dans les routes API"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f'Error in {f.__name__}: {str(e)}')
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    return decorated_function

def require_json(f):
    """Décorateur pour vérifier le Content-Type JSON"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
        return f(*args, **kwargs)
    return decorated_function
