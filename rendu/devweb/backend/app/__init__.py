"""
Initialisation de l'application Flask
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

def create_app(config_name=None):
    """
    Factory pour créer l'instance Flask
    
    Args:
        config_name: 'development', 'production', 'testing'
    """
    app = Flask(
        __name__,
        template_folder="../../frontend/templates",
        static_folder="../../frontend/static"
    )    
    # Configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Base de données
    from app.models import db
    db.init_app(app)
    
    # Logger
    from app.utils.logger import setup_logger
    setup_logger(app)
    
    # Routes
    from app.routes import register_blueprints
    register_blueprints(app)
    
    # Context d'application pour les commandes CLI
    with app.app_context():
        db.create_all()
    
    # CORS pour les requêtes cross-origin
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    
    app.logger.info(f'Application initialized with config: {config_name}')
    
    return app
