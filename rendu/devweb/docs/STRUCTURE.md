# 🏗️ STRUCTURE DU PROJET

```
rendu/devweb/
│
├── 📄 docs/                          # 📖 Documentation
│   ├── INDEX.md                      # Point d'entrée documentation
│   ├── README.md                     # Complet et détaillé
│   ├── QUICKSTART.md                 # Démarrage 5 minutes
│   ├── ARCHITECTURE.md               # Détails techniques
│   └── STRUCTURE.md                  # Ce fichier
│
├── 🐍 backend/                       # 🔧 Backend Flask
│   ├── run.py                        # Point d'entrée
│   ├── requirements.txt              # Dépendances Python
│   ├── .env.example                  # Configuration exemple
│   ├── app/                          # 🎯 Cœur de l'app
│   │   ├── __init__.py              # Factory Flask
│   │   ├── config.py                # Configuration centralisée
│   │   │
│   │   ├── models/
│   │   │   └── __init__.py          # SQLAlchemy models
│   │   │       ├── Session          # Modèle Session
│   │   │       └── Message          # Modèle Message
│   │   │
│   │   ├── services/
│   │   │   ├── ollama_service.py    # Service Ollama
│   │   │   └── chat_service.py      # Logique chat
│   │   │
│   │   ├── routes/
│   │   │   ├── __init__.py          # Enregistrement blueprints
│   │   │   ├── chat.py              # Endpoints chat
│   │   │   ├── health.py            # Health checks
│   │   │   └── web.py               # Routes web
│   │   │
│   │   ├── utils/
│   │   │   ├── logger.py            # Configuration logging
│   │   │   └── decorators.py        # Décorateurs réutilisables
│   │   │
│   │   └── logs/                    # 📋 Fichiers logs
│   │       └── app.log
│   │
│   └── venv/                        # Python virtualenv (ignoré)
│
├── 🎨 frontend/                      # 🖼️ Interface Web
│   ├── templates/
│   │   └── index.html               # Interface principale
│   │
│   └── static/
│       ├── css/
│       │   └── style.css            # Design moderne
│       │
│       └── js/
│           └── app.js               # ChatManager, ApiClient
│
├── 🚀 deploy/                        # 📦 Déploiement
│   ├── start.bat                    # Démarrage Windows
│   ├── start.sh                     # Démarrage Linux/Mac
│   ├── Dockerfile                   # Image Docker
│   ├── docker-compose.yml           # Stack Docker
│   └── .gitignore                   # Fichiers ignorés
│
├── 🧪 tests/                        # ✅ Tests
│   ├── test_app.py                  # Tests unitaires
│   └── examples.py                  # Exemples d'utilisation
│
└── 📊 root files                     # Fichiers racine
    ├── chat_history.db              # 🗄️ Base de données (généré)
    └── .env                         # Configuration active (généré)
```

## 📂 Description des Dossiers

### 📄 `docs/`
Documentation du projet
- INDEX.md : Point d'entrée, guide rapide
- README.md : Documentation complète
- QUICKSTART.md : Démarrage rapide
- ARCHITECTURE.md : Détails techniques

### 🐍 `backend/`
Code backend Flask
- `run.py` : Point d'entrée de l'app
- `requirements.txt` : Dépendances Python
- `.env.example` : Configuration exemple
- `app/` : Code source de l'application
  - models/ : Schémas de données
  - services/ : Logique métier
  - routes/ : Endpoints API
  - utils/ : Code réutilisable

### 🎨 `frontend/`
Code frontend (HTML/CSS/JS)
- `templates/` : Templates HTML
- `static/` : Assets statiques (CSS, JS)

### 🚀 `deploy/`
Configuration de déploiement
- Scripts de démarrage (start.bat, start.sh)
- Docker (Dockerfile, docker-compose.yml)
- .gitignore : Fichiers ignorés

### 🧪 `tests/`
Tests et exemples
- `test_app.py` : Tests unitaires
- `examples.py` : Exemples d'utilisation

## 🔄 Comment Utiliser Cette Structure

### Installation
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```

### Développement
```bash
# Point d'entrée
cd backend
python run.py

# Ou avec les scripts
deploy/start.bat   # Windows
deploy/start.sh    # Linux/Mac
```

### Tests
```bash
cd tests
python test_app.py      # Tests unitaires
python examples.py      # Exemples
```

### Déploiement
```bash
# Docker
docker-compose -f deploy/docker-compose.yml up

# Production
cd backend
pip install -r requirements.txt
python run.py
```

## 📁 Fichiers Clés

| Fichier | Purpose |
|---------|---------|
| `backend/run.py` | Point d'entrée Flask |
| `backend/app/__init__.py` | Factory Flask |
| `backend/app/config.py` | Configuration centralisée |
| `backend/app/models/__init__.py` | Schémas BD |
| `backend/app/services/ollama_service.py` | Logique Ollama |
| `backend/app/services/chat_service.py` | Logique chat |
| `backend/app/routes/chat.py` | Endpoints chat |
| `frontend/templates/index.html` | Interface |
| `frontend/static/js/app.js` | Logique client |
| `frontend/static/css/style.css` | Styles |
| `deploy/Dockerfile` | Image Docker |
| `deploy/start.bat` | Démarrage Windows |
| `deploy/start.sh` | Démarrage Linux/Mac |
| `tests/test_app.py` | Tests unitaires |
| `tests/examples.py` | Exemples |

## 🎯 Bonnes Pratiques

1. **Configuration** : Utiliser `.env` pour les variables sensibles
2. **Logging** : Écrire dans `backend/app/logs/app.log`
3. **BD** : SQLite en développement, PostgreSQL en production
4. **Frontend** : Fichiers statiques dans `frontend/static/`
5. **Tests** : Écrire les tests dans `tests/`
6. **Docs** : Tenir à jour `docs/README.md`

---

**🚀 Prêt à démarrer ?** → Voir [docs/QUICKSTART.md](./docs/QUICKSTART.md)
