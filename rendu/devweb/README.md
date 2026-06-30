# 🚀 Assistant Financier - DEV WEB

> Démarrage rapide : [📖 Voir la documentation](./docs/INDEX.md)

## ⚡ Démarrage en 30 secondes

### Windows
```bash
deploy\start.bat
```

### Linux/Mac
```bash
chmod +x deploy/start.sh
./deploy/start.sh
```

Puis accédez à : **http://localhost:5000**

---

## 📁 Structure du Projet

```
rendu/devweb/
├── 📄 docs/                  # 📖 Documentation complète
│   ├── INDEX.md             # 👈 Commencez ici
│   ├── README.md            # Documentation générale
│   ├── QUICKSTART.md        # Démarrage rapide
│   ├── ARCHITECTURE.md      # Architecture détaillée
│   └── STRUCTURE.md         # Organisation du code
│
├── 🐍 backend/              # Code Flask
│   ├── run.py              # Point d'entrée
│   ├── requirements.txt    # Dépendances
│   ├── .env.example        # Config exemple
│   └── app/                # Application Flask
│
├── 🎨 frontend/            # Interface Web
│   ├── templates/          # HTML
│   └── static/             # CSS & JS
│
├── 🚀 deploy/              # Déploiement
│   ├── start.bat          # Lancer (Windows)
│   ├── start.sh           # Lancer (Linux/Mac)
│   ├── Dockerfile         # Image Docker
│   └── docker-compose.yml # Stack Docker
│
├── 🧪 tests/              # Tests & Exemples
    ├── test_app.py       # Tests unitaires
    └── examples.py       # Exemples d'utilisation
```

---

## 📖 Documentation

- **[docs/INDEX.md](./docs/INDEX.md)** - Index et points d'entrée
- **[docs/README.md](./docs/README.md)** - Documentation complète
- **[docs/QUICKSTART.md](./docs/QUICKSTART.md)** - Démarrage rapide (5 min)
- **[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)** - Architecture détaillée
- **[docs/STRUCTURE.md](./docs/STRUCTURE.md)** - Organisation du code

---

## ✅ Prérequis

- ✅ Python 3.8+
- ✅ Ollama lancé (`ollama serve`)
- ✅ Modèle `phi3_financial` chargé

---

## 🔗 Endpoints API

- `POST /api/chat/message` - Envoyer un message
- `GET /api/chat/history/<id>` - Historique
- `GET /api/health` - État du serveur
- `GET /` - Interface web

---

## 🚀 Commandes Utiles

```bash
# Démarrer l'application
deploy/start.bat              # Windows
./deploy/start.sh            # Linux/Mac

# Tests
python tests/test_app.py     # Tests unitaires
python tests/examples.py     # Exemples

# Déploiement Docker
docker-compose -f deploy/docker-compose.yml up
```

---

## 🐛 Troubleshooting

| Problème | Solution |
|----------|----------|
| Ollama déconnecté | Lancer `ollama serve` |
| Port 5000 occupé | Utiliser `PORT=5001 python run.py` |
| Module non trouvé | Lancer depuis `backend/`: `cd backend && python run.py` |
| Erreur BD | Supprimer `chat_history.db` |

---

## 📞 Support

Consultez [docs/README.md](./docs/README.md) pour une documentation complète.

---

**🎉 Prêt à commencer ?** → [Voir la documentation](./docs/INDEX.md)
