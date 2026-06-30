#!/usr/bin/env python3
"""
Exemples d'utilisation de l'API
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

class ChatClient:
    """Client simple pour tester l'API"""
    
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session_id = f"example_{int(time.time())}"
    
    def check_health(self):
        """Vérifier la santé du serveur"""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def send_message(self, message):
        """Envoyer un message"""
        try:
            response = requests.post(
                f"{self.base_url}/chat/message",
                json={
                    "session_id": self.session_id,
                    "message": message
                }
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_history(self):
        """Récupérer l'historique"""
        try:
            response = requests.get(f"{self.base_url}/chat/history/{self.session_id}")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def list_sessions(self):
        """Lister toutes les sessions"""
        try:
            response = requests.get(f"{self.base_url}/chat/sessions")
            return response.json()
        except Exception as e:
            return {"error": str(e)}

def print_response(title, data):
    """Afficher une réponse formatée"""
    print(f"\n{'='*60}")
    print(f"🔹 {title}")
    print(f"{'='*60}")
    print(json.dumps(data, indent=2, ensure_ascii=False))

def main():
    """Exemples d'utilisation"""
    
    client = ChatClient()
    
    print("\n🚀 Exemples d'Utilisation de l'API Assistant Financier")
    
    # 1. Vérifier la santé
    print("\n1️⃣ Vérification de la santé du serveur...")
    health = client.check_health()
    print_response("Health Check", health)
    
    if health.get("ollama") != "connected":
        print("\n❌ Ollama n'est pas connecté. Assurez-vous qu'Ollama est lancé.")
        return
    
    # 2. Envoyer un message
    print("\n2️⃣ Envoi d'un message...")
    result = client.send_message("Explique-moi brièvement les bases du trading")
    print_response("Réponse du Modèle", result)
    
    if not result.get("success"):
        print("\n❌ Erreur lors de l'envoi du message")
        return
    
    time.sleep(1)
    
    # 3. Deuxième message
    print("\n3️⃣ Envoi d'un deuxième message...")
    result = client.send_message("Quel est le risque du trading?")
    print_response("Deuxième Réponse", result)
    
    # 4. Récupérer l'historique
    print("\n4️⃣ Récupération de l'historique...")
    history = client.get_history()
    print_response("Historique de la Session", history)
    
    # 5. Lister toutes les sessions
    print("\n5️⃣ Listage de toutes les sessions...")
    sessions = client.list_sessions()
    print_response("Sessions", sessions)
    
    print("\n✅ Exemples terminés !")
    print(f"\n💡 Session ID : {client.session_id}")
    print(f"🌐 Interface Web : http://localhost:5000")

if __name__ == "__main__":
    main()
