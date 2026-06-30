# 🚀 Assistant Financier - Interface Web Professionnelle

Application web Flask moderne et scalable pour interagir avec le modèle Phi-3.5-Financial via l'API Ollama.

> Pour démarrer rapidement, voir [QUICKSTART.md](./QUICKSTART.md)

## 📊 Architecture

L'application suit une architecture en **couches** pour une meilleure maintenabilité :

```
Navigateur (HTML/CSS/JS)
        ↓
    Routes (Validation)
        ↓
    Services (Logique Métier)
        ↓
    Models (Base de Données)
        ↓
    SQLite Database
    
    + Appels à Ollama API
```

## 🏗️ Principes d'Architecture

### Séparation des Préoccupations
- **Routes** : Endpoints API uniquement (validation)
- **Services** : Logique métier isolée (Ollama, Chat)
- **Models** : Schémas de données avec SQLAlchemy
- **Utils** : Code réutilisable (décorateurs, logging)

### Avantages
✅ **Maintenabilité** : Chaque couche a une responsabilité unique  
✅ **Testabilité** : Services faciles à tester en isolation  
✅ **Scalabilité** : Facile d'ajouter de nouveaux endpoints  
✅ **Réutilisabilité** : Services utilisables partout  
✅ **Documenté** : Docstrings clairs partout  

## 🚀 Démarrage Rapide

### 1. Installation

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```

### 2. Configuration

Éditer `backend/.env` si nécessaire (par défaut OK) :

```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=phi3_financial
FLASK_ENV=development
```

### 3. Démarrage

```bash
# Option 1 : Script automatique (recommandé)
deploy/start.bat              # Windows
./deploy/start.sh            # Linux/Mac

# Option 2 : Manuel
cd backend
python run.py
```

L'application sera disponible sur : **http://localhost:5000**

## 📡 API Endpoints

### Chat

**POST** `/api/chat/message`
```json
{
  "session_id": "uuid (optionnel)",
  "message": "Votre question"
}
```
Retour : Message utilisateur + réponse du modèle

**GET** `/api/chat/history/<session_id>`  
Récupère l'historique d'une session

**GET** `/api/chat/sessions`  
Liste toutes les sessions

**DELETE** `/api/chat/session/<session_id>`  
Supprime une session

### Health

**GET** `/api/health`  
État du serveur et connexion Ollama

**GET** `/api/status`  
Statut complet

### Web

**GET** `/`  
Interface chat principale

## 🗄️ Base de Données

SQLite locale avec deux modèles :

### Session
- `id` (String, PK)
- `created_at` (DateTime)
- `updated_at` (DateTime)
- Relation: `messages[]`

### Message
- `id` (Integer, PK)
- `session_id` (FK → Session)
- `role` ('user' | 'assistant')
- `content` (Text)
- `timestamp` (DateTime)

## 🎨 Interface Utilisateur

- **Responsive Design** : Mobile-friendly
- **Mode Dark/Light** : Via CSS variables
- **Real-time Chat** : Avec animations
- **Session Management** : Barre latérale historique
- **Status Indicator** : État de connexion Ollama

## ⚙️ Configuration

Fichier `backend/.env` :

```env
# Ollama
OLLAMA_HOST=http://localhost:11434      # Adresse du serveur
OLLAMA_MODEL=phi3_financial             # Modèle à utiliser
OLLAMA_TIMEOUT=60                       # Timeout en secondes

# Flask
FLASK_ENV=development                   # development/production
FLASK_DEBUG=True                        # Debug mode
SECRET_KEY=your-secret-key-here         # Secret pour sessions

# Base de données
DATABASE_URL=sqlite:///chat_history.db  # Connexion BD

# Logging
LOG_LEVEL=INFO                          # DEBUG/INFO/WARNING/ERROR
```

## 📝 Logging

Les logs sont écrits dans `backend/app/logs/app.log` avec rotation automatique (10MB max).

### Structure des logs
```
2026-06-30 10:30:45,123 INFO: Message utilisateur reçu [in routes/chat.py:45]
2026-06-30 10:30:46,456 INFO: Réponse générée [in services/ollama_service.py:78]
```

## 📚 Services

### OllamaService (`backend/app/services/ollama_service.py`)

Interaction avec Ollama :
- `check_health()` : Vérifier la connexion
- `generate(prompt)` : Générer une réponse
- `list_models()` : Lister les modèles

### ChatService (`backend/app/services/chat_service.py`)

Gestion des conversations :
- `create_session(id)` : Créer une session
- `get_or_create_session(id)` : Récupérer ou créer
- `add_message(session_id, role, content)` : Ajouter un message
- `process_message(session_id, message)` : Traitement complet
- `get_history(session_id)` : Récupérer historique
- `delete_session(session_id)` : Supprimer session
- `get_all_sessions()` : Lister sessions

## 🔧 Utilitaires

### Décorateurs (`backend/app/utils/decorators.py`)

- `@handle_errors` : Gestion centralisée des erreurs
- `@require_json` : Validation Content-Type JSON

### Logger (`backend/app/utils/logger.py`)

Configuration de logging production-ready avec rotation de fichiers.

## 🧪 Testing

### Tests Unitaires

```bash
cd tests
python test_app.py
```

Tests disponibles :
- Endpoints HTTP
- Modèles SQLAlchemy
- Validation des données

### Exemples d'Utilisation

```bash
cd tests
python examples.py
```

Démontre :
- Health check
- Envoi de messages
- Récupération d'historique
- Liste des sessions

### Tests Manuels

```bash
# Via cURL
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test_001","message":"Bonjour!"}'

# Réponse
{
  "success": true,
  "session_id": "test_001",
  "user_message": "Bonjour!",
  "bot_response": "..."
}
```

## 🐛 Troubleshooting

### "Ollama déconnecté"
```bash
# Vérifier que Ollama est lancé
ollama serve

# Vérifier la connexion
curl http://localhost:11434/api/tags
```

### "Erreur 500"
```bash
# Vérifier les logs
tail -f backend/app/logs/app.log

# Redémarrer l'app
python backend/run.py
```

### "Port 5000 déjà utilisé"
```bash
# Changer le port
PORT=5001 python backend/run.py
```

### "Erreur de base de données"
```bash
# Réinitialiser la BD
rm chat_history.db
python backend/run.py  # Créera une nouvelle BD
```

## 🚀 Production

### Avec Gunicorn

```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Avec Docker

```bash
docker-compose -f deploy/docker-compose.yml up
```

### Environnement Production

Configurer `backend/.env` :
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=generate-a-strong-key
DATABASE_URL=postgresql://user:pass@host/db
```

## 📦 Dépendances

### Backend
- **Flask** 3.0.0 : Framework web
- **Flask-SQLAlchemy** 3.1.1 : ORM
- **Requests** 2.31.0 : Client HTTP
- **python-dotenv** 1.0.0 : Gestion env
- **gunicorn** 21.2.0 : Production server

### Versions
- Python 3.8+
- SQLite 3.x

## 💡 Améliorations Futures

- [ ] Authentification utilisateur
- [ ] Stockage utilisateur des sessions
- [ ] Export conversations (PDF/JSON)
- [ ] Paramètres de génération (temperature, top_p)
- [ ] Historique recherche avancée
- [ ] WebSocket pour real-time streaming
- [ ] Cache avec Redis
- [ ] Monitoring & metrics
- [ ] Rate limiting
- [ ] API versioning (/api/v1/)

## 📄 Licence

Hackathon TechCorp Industries 2026

## 🤝 Support

Pour des questions ou problèmes :
1. Consulter [QUICKSTART.md](./QUICKSTART.md)
2. Vérifier les logs : `backend/app/logs/app.log`
3. Lire [ARCHITECTURE.md](./ARCHITECTURE.md) pour les détails

---

**À lire ensuite :**
- [QUICKSTART.md](./QUICKSTART.md) - Démarrage rapide
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Détails techniques
- [STRUCTURE.md](./STRUCTURE.md) - Organisation du code
