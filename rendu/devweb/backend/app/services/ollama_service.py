"""
Service pour l'interaction avec Ollama
"""
import requests
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class OllamaService:
    """Service pour communiquer avec le serveur Ollama"""
    
    @staticmethod
    def check_health():
        """Vérifier que le serveur Ollama est accessible"""
        try:
            response = requests.get(
                f"{current_app.config['OLLAMA_HOST']}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama health check failed: {str(e)}")
            return False
    
    @staticmethod
    def generate(prompt: str) -> str:
        """
        Générer une réponse du modèle Ollama
        
        Args:
            prompt: Le texte d'entrée
            
        Returns:
            La réponse du modèle
            
        Raises:
            Exception: Si la requête échoue
        """
        try:
            url = f"{current_app.config['OLLAMA_HOST']}/api/generate"
            
            payload = {
                "model": current_app.config['OLLAMA_MODEL'],
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(
                url,
                json=payload,
                timeout=current_app.config['OLLAMA_TIMEOUT']
            )
            
            response.raise_for_status()
            result = response.json()
            
            return result.get('response', '')
        
        except requests.exceptions.Timeout:
            logger.error("Ollama request timeout")
            raise Exception("Modèle lent - timeout. Vérifiez que Ollama répond.")
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Ollama")
            raise Exception("Impossible de se connecter à Ollama. Vérifiez la configuration.")
        except Exception as e:
            logger.error(f"Ollama error: {str(e)}")
            raise Exception(f"Erreur modèle: {str(e)}")
    
    @staticmethod
    def list_models():
        """Lister les modèles disponibles"""
        try:
            response = requests.get(
                f"{current_app.config['OLLAMA_HOST']}/api/tags",
                timeout=5
            )
            response.raise_for_status()
            return response.json().get('models', [])
        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
            return []
