"""
Routes de l'application
"""
from flask import Blueprint

def register_blueprints(app):
    """Enregistrer tous les blueprints"""
    from app.routes.chat import chat_bp
    from app.routes.health import health_bp
    from app.routes.web import web_bp
    
    app.register_blueprint(chat_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(web_bp)
