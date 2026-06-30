"""
Configuration du logging
"""
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(app):
    """Configure le logger pour l'application"""
    
    # Créer dossier logs s'il n'existe pas
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Handler fichier
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    
    # Format des logs
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(formatter)
    
    # Niveau de log
    file_handler.setLevel(getattr(logging, app.config.get('LOG_LEVEL', 'INFO')))
    
    # Ajouter au logger Flask
    app.logger.addHandler(file_handler)
    app.logger.setLevel(getattr(logging, app.config.get('LOG_LEVEL', 'INFO')))
    
    app.logger.info('Application startup')
