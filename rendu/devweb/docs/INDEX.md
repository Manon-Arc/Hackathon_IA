# 📚 INDEX DE DOCUMENTATION

## 🚀 Pour Démarrer Rapidement
- **[QUICKSTART.md](./QUICKSTART.md)** - Démarrage en 5 minutes

## 📖 Documentation Principale
- **[README.md](./README.md)** - Documentation complète (architecture, API, config)
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Détails techniques et diagrammes

## 💻 Fichiers importants

- **[../backend/run.py](../backend/run.py)** - Point d'entrée
- **[../backend/requirements.txt](../backend/requirements.txt)** - Dépendances
- **[../backend/.env.example](../backend/.env.example)** - Configuration

## 🔗 Endpoints API

### Chat
- `POST /api/chat/message` - Envoyer un message
- `GET /api/chat/history/<id>` - Historique
- `GET /api/chat/sessions` - Lister sessions
- `DELETE /api/chat/session/<id>` - Supprimer session

### Health
- `GET /api/health` - État serveur
- `GET /api/status` - Statut complet

### Web
- `GET /` - Interface chat

## 🧪 Testing

```bash
# Tests unitaires
python tests/test_app.py

# Exemples d'utilisation
python tests/examples.py

# Manuel via cURL
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test","message":"Bonjour"}'
```

## 🚀 Démarrage

**Windows**
```bash
deploy/start.bat
```

**Linux/Mac**
```bash
chmod +x deploy/start.sh
deploy/start.sh
```

## 📊 Structure Complète

Voir [STRUCTURE.md](./STRUCTURE.md) pour l'organisation détaillée des dossiers.

## 🐛 Troubleshooting

1. **Ollama déconnecté** → Vérifier `ollama serve`
2. **Port occupé** → Changer PORT=5001
3. **Erreur BD** → Supprimer `*.db`
4. **Logs** → Voir `logs/app.log`

---

**Prêt à commencer ?** → [QUICKSTART.md](./QUICKSTART.md)
