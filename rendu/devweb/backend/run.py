#!/usr/bin/env python3
"""
Point d'entrée de l'application
"""
import os
from app import create_app

# Créer l'app
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5005))
    app.run(host='0.0.0.0', port=port, debug=app.debug)
