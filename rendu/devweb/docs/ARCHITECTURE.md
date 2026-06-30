# 🏗️ ARCHITECTURE DÉTAILLÉE

## 📊 Diagramme de Flux Complet

```
┌─────────────────────────────────────────────────────────────┐
│                    NAVIGATEUR WEB                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  index.html + app.js (ChatManager)                   │   │
│  │  - Interface chat                                    │   │
│  │  - Gestion des sessions                              │   │
│  │  - Appels API asynchrones                            │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────┬────────────────────────────────────────────────┘
             │ HTTP/JSON
             ▼
┌─────────────────────────────────────────────────────────────┐
│              SERVEUR FLASK (backend/run.py)                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Routes (routes/*.py)                                 │   │
│  │ ├── POST /api/chat/message ──┐                      │   │
│  │ ├── GET  /api/chat/history   ├──> ChatService      │   │
│  │ ├── GET  /api/chat/sessions  │    (chat_service.py)│   │
│  │ ├── GET  /api/health         ├──> OllamaService    │   │
│  │ └── GET  / (index.html)      │    (ollama_service) │   │
│  └──────────────┬────────────────────────────────────┘   │
│                 │                                        │
│  ┌──────────────▼────────────────────────────────────┐   │
│  │ Services (services/*.py)                           │   │
│  │ ├── ChatService: Gestion des conversations        │   │
│  │ └── OllamaService: Appels au modèle               │   │
│  └──────────────┬────────────────────────────────────┘   │
│                 │                                        │
│  ┌──────────────▼────────────────────────────────────┐   │
│  │ Models (models/__init__.py - SQLAlchemy)          │   │
│  │ ├── Session (UUID, created_at, updated_at)        │   │
│  │ └── Message (role, content, timestamp)            │   │
│  └──────────────┬────────────────────────────────────┘   │
│                 │                                        │
│  ┌──────────────▼────────────────────────────────────┐   │
│  │ Utilities (utils/*.py)                             │   │
│  │ ├── Logger: Configuration logging                  │   │
│  │ └── Decorators: @handle_errors, @require_json      │   │
│  └──────────────┬────────────────────────────────────┘   │
│                 │                                        │
│  ┌──────────────▼────────────────────────────────────┐   │
│  │ Database (SQLite)                                  │   │
│  │ └── chat_history.db                               │   │
│  └──────────────────────────────────────────────────┘   │
└────────────┬────────────────────────────────────────────────┘
             │ HTTP/API
             ▼
┌─────────────────────────────────────────────────────────────┐
│                OLLAMA SERVER (localhost:11434)              │
│  ├── /api/tags (list models)                               │
│  ├── /api/generate (inference)                             │
│  └── Phi-3.5-Financial (modèle)                            │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Flux d'une Requête Message

```
1. Utilisateur tape un message dans l'UI
   │
2. ChatManager.sendMessage() 
   ├── Affiche le message utilisateur immédiatement
   ├── Active le loader
   └── Appelle ApiClient.sendMessage()
   │
3. ApiClient.sendMessage()
   └── POST /api/chat/message
       {
         "session_id": "session_123",
         "message": "Bonjour"
       }
   │
4. Route chat.py (@require_json, @handle_errors)
   ├── Valide le JSON
   ├── Appelle ChatService.process_message()
   └── Retourne la réponse
   │
5. ChatService.process_message()
   ├── add_message(session_id, 'user', message)
   │   └── Sauvegarde le message utilisateur en BD
   ├── OllamaService.generate(message)
   │   └── Appelle Ollama pour générer une réponse
   ├── add_message(session_id, 'assistant', response)
   │   └── Sauvegarde la réponse en BD
   └── Retourne le résultat
   │
6. Réponse JSON au client
   {
     "success": true,
     "session_id": "session_123",
     "user_message": "Bonjour",
     "bot_response": "Réponse du modèle..."
   }
   │
7. ChatManager reçoit la réponse
   ├── Retire le loader
   ├── Affiche la réponse de l'assistant
   └── Met à jour l'historique
```

## 📦 Séparation des Responsabilités

### Routes (`backend/app/routes/*.py`)
```python
# Responsabilités:
- Valider les requêtes HTTP
- Appeler les services appropriés
- Retourner des réponses JSON
- Gérer les codes HTTP

# Limitation:
- PAS de logique métier complexe
- PAS d'accès direct à la BD
```

### Services (`backend/app/services/*.py`)
```python
# Responsabilités:
- Logique métier (OllamaService, ChatService)
- Orchestration des opérations
- Gestion des erreurs métier
- Appels à la BD via Models

# Limitation:
- PAS de formatage HTTP
- PAS d'accès direct aux requêtes
```

### Models (`backend/app/models/__init__.py`)
```python
# Responsabilités:
- Définition des schémas de données
- Relations entre entités
- Validation des données
- Queries simples via ORM

# Limitation:
- PAS de logique métier
- PAS d'appels API
```

### Utils (`backend/app/utils/*.py`)
```python
# Responsabilités:
- Code réutilisable (décorateurs, logging)
- Configuration centralisée
- Helpers techniques

# Limitation:
- Code spécifique au domaine ailleurs
```

## 🔀 Différents Flux Selon l'Endpoint

### 1. GET / (Interface Web)
```
Route(web.py) → render_template('index.html')
                    ↓
            Frontend (HTML/CSS/JS)
```

### 2. POST /api/chat/message
```
Route(chat.py) @require_json @handle_errors
    ↓
ChatService.process_message()
    ├── add_message (sauve utilisateur)
    ├── OllamaService.generate (appelle le modèle)
    └── add_message (sauve assistant)
    ↓
Retourne JSON {success, session_id, messages}
```

### 3. GET /api/health
```
Route(health.py)
    ↓
OllamaService.check_health()
    ↓
Retourne {status, ollama_connected, models}
```

### 4. GET /api/chat/history/<session_id>
```
Route(chat.py)
    ↓
ChatService.get_history()
    ↓
Query BD → Message[] 
    ↓
Retourne JSON {session_id, messages}
```

## 🗄️ Schéma Base de Données

```sql
-- Modèle Session
CREATE TABLE sessions (
    id VARCHAR(36) PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Modèle Message
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(36) NOT NULL,
    role VARCHAR(20) NOT NULL,  -- 'user' ou 'assistant'
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

-- Index pour les requêtes fréquentes
CREATE INDEX idx_messages_session 
    ON messages(session_id);
```

## 🎯 Étapes d'une Requête Complète

### 1. Initialisation (backend/app/__init__.py)
```
create_app()
├── Charger config (config.py)
├── Initialiser DB (models.py)
├── Setup logging (utils/logger.py)
├── Enregistrer routes (routes/__init__.py)
└── Retourner app Flask
```

### 2. Requête HTTP Entrante
```
request → Flask routing
├── Matcher route (routes/*.py)
├── Exécuter @decorators
│   ├── @require_json (valider Content-Type)
│   └── @handle_errors (try/catch)
└── Exécuter handler (fonction route)
```

### 3. Appel Service
```
Handler → Service
├── Service accède BD (via Models/SQLAlchemy)
├── Service appelle autres services
└── Service retourne résultat
```

### 4. Formatage Réponse
```
Résultat → jsonify()
├── Convertir en JSON
├── Ajouter headers CORS
└── Retourner au client
```

## 💡 Avantages de Cette Architecture

| Avantage | Description |
|----------|-------------|
| **Testabilité** | Services isolés = tests unitaires faciles |
| **Maintenabilité** | Chaque couche a une responsabilité claire |
| **Scalabilité** | Facile d'ajouter/modifier sans affecter le reste |
| **Réutilisabilité** | Services utilisables par d'autres routes |
| **Évolutivité** | BD/Ollama changeable sans toucher le reste |
| **Documentation** | Structure auto-documentante |
| **Debugging** | Isoler les bugs par couche |
| **Testing** | Mock des services facilement |

## 🚀 Points d'Amélioration Possibles

1. **Caching** : Redis pour les requêtes fréquentes
2. **Async** : AsyncIO pour les appels Ollama (streaming)
3. **Auth** : Authentification utilisateur
4. **Monitoring** : Prometheus/Grafana pour les métriques
5. **Testing** : Suite de tests plus complète
6. **Versioning API** : /api/v1/ pour évolutions futures
7. **Rate Limiting** : Protection contre abus
8. **Message Queue** : Celery pour tâches longues
9. **WebSockets** : Pour streaming en temps réel
10. **CDN** : Pour les assets statiques

## 📝 Fichiers Clés à Comprendre

```
backend/
├── run.py                          # Point d'entrée
├── app/__init__.py                 # Factory Flask
├── app/config.py                   # Configuration
├── app/models/__init__.py          # Schémas données
├── app/services/ollama_service.py  # Logique Ollama
├── app/services/chat_service.py    # Logique métier
├── app/routes/chat.py              # Endpoints chat
├── app/routes/health.py            # Health checks
├── app/routes/web.py               # Routes web
├── app/utils/decorators.py         # Décorateurs
└── app/utils/logger.py             # Configuration logs

frontend/
├── templates/index.html            # Interface
└── static/
    ├── css/style.css              # Styles
    └── js/app.js                  # Logique client
```

---

**Bienvenue dans une architecture professionnelle !** 🎯

Pour plus d'infos, voir [STRUCTURE.md](./STRUCTURE.md)
