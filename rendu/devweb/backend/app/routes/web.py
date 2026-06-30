"""
Route pour servir l'interface web
"""
from flask import Blueprint, render_template

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def index():
    """Page principale du chat"""
    return render_template('index.html')
