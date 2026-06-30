# 🎯 GUIDE DE DÉMARRAGE RAPIDE - DEV WEB

## ⚡ 5 Minutes pour Démarrer

### Prérequis
- ✅ Python 3.8+
- ✅ Serveur Ollama lancé sur `http://localhost:11434`
- ✅ Modèle `phi3_financial` chargé

### Windows
```bash
cd rendu\devweb
deploy\start.bat
```

### Linux/Mac
```bash
cd rendu/devweb
chmod +x deploy/start.sh
./deploy/start.sh
```

### Accès
```
http://localhost:5000
```

---

## 🔗 Vérifier la Configuration

### 1. Tester Ollama
```bash
curl http://localhost:11434/api/tags
```

### 2. Tester l'API
```bash
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test_001",
    "message": "Bonjour!"
  }'
```

### 3. Réponse attendue
```json
{
  "success": true,
  "session_id": "test_001",
  "user_message": "Bonjour!",
  "bot_response": "..."
}
```

---

## 📋 Installation Manuelle

Si les scripts ne fonctionnent pas :

```bash
# 1. Aller dans le dossier backend
cd rendu/devweb/backend

# 2. Créer virtualenv
python -m venv venv

# 3. Activer virtualenv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Installer dépendances
pip install -r requirements.txt

# 5. Copier configuration
cp .env.example .env

# 6. Démarrer l'app
python run.py
```

---

## 🚀 Démarrage Production

### Avec Docker (recommandé)

```bash
cd rendu/devweb
docker-compose -f deploy/docker-compose.yml up
```

### Avec Gunicorn

```bash
cd rendu/devweb/backend
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

---

## 🧪 Tests Rapides

### Lancer les exemples
```bash
cd rendu/devweb/tests
python examples.py
```

### Tests unitaires
```bash
cd rendu/devweb/tests
python test_app.py
```

---

## 🐛 Dépannage

| Problème | Solution |
|----------|----------|
| **Ollama déconnecté** | `ollama serve` dans un autre terminal |
| **Port 5000 utilisé** | `PORT=5001 python run.py` |
| **Erreur "permission denied"** | `chmod +x deploy/start.sh` (Linux/Mac) |
| **Module non trouvé** | `pip install -r requirements.txt` |
| **BD corrompue** | `rm chat_history.db` puis relancer |
| **Logs** | Voir `backend/app/logs/app.log` |

---

## 📊 Architecture Rapide

```
Navigateur (HTML/CSS/JS)
        ↓ HTTP/JSON
    Flask API
    ├── Routes (validation)
    ├── Services (logique)
    ├── Models (BD)
    └── Utils
        ↓
    SQLite DB
    
    + Appels Ollama API
```

---

## 🔑 Endpoints Principaux

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/chat/message` | Envoyer un message |
| GET | `/api/chat/history/<id>` | Historique |
| GET | `/api/chat/sessions` | Toutes les sessions |
| GET | `/api/health` | État serveur |
| GET | `/` | Interface web |

---

## ⚙️ Configuration

Fichier `backend/.env` :

```env
# Ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=phi3_financial

# Flask
FLASK_ENV=development
SECRET_KEY=dev-key

# BD
DATABASE_URL=sqlite:///chat_history.db
```

---

## 📁 Fichiers Importants

```
backend/
├── run.py                    ← Point d'entrée
├── requirements.txt          ← Dépendances
├── .env                      ← Configuration (généré)
├── .env.example              ← Template config
├── app/
│   ├── __init__.py          ← Factory Flask
│   ├── config.py            ← Config centralisée
│   ├── models/              ← Schémas BD
│   ├── services/            ← Logique métier
│   ├── routes/              ← Endpoints
│   └── utils/               ← Helpers
└── logs/
    └── app.log              ← Fichier logs
```

---

## 📚 Documentation Complète

- [README.md](./README.md) - Documentation générale
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Détails techniques
- [STRUCTURE.md](./STRUCTURE.md) - Organisation du code

---

## ✅ Checklist

- [ ] Ollama lancé et accessible
- [ ] Python 3.8+ installé
- [ ] `cd rendu/devweb`
- [ ] Exécuter `deploy/start.bat` ou `deploy/start.sh`
- [ ] Accéder à http://localhost:5000
- [ ] Interface accessible ✅

**C'est prêt !** 🎉
