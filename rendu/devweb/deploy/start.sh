#!/bin/bash
# =====================================================
# Script de démarrage - Assistant Financier
# =====================================================

set -e

echo "======================================================"
echo "🚀 Démarrage de l'Assistant Financier"
echo "======================================================"
echo

# =====================================================
# Se placer à la racine du projet
# =====================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "📂 Répertoire du projet :"
echo "   $PROJECT_ROOT"
echo

# =====================================================
# Vérification de Python
# =====================================================

echo "[1/6] Vérification de Python..."

if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ Python 3 n'est pas installé."
    exit 1
fi

python3 --version
echo

# =====================================================
# Création du venv
# =====================================================

echo "[2/6] Vérification de l'environnement virtuel..."

if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
    echo "✅ Environnement virtuel créé."
else
    echo "✅ Environnement virtuel déjà présent."
fi

echo

# =====================================================
# Activation
# =====================================================

echo "[3/6] Activation de l'environnement virtuel..."

source venv/bin/activate

echo "✅ Environnement activé."
echo

# =====================================================
# Installation des dépendances
# =====================================================

echo "[4/6] Installation des dépendances..."

python -m pip install --upgrade pip

pip install -r backend/requirements.txt

echo "✅ Dépendances installées."
echo

# =====================================================
# Configuration
# =====================================================

echo "[5/6] Vérification du fichier .env..."

if [ ! -f "backend/.env" ]; then
    if [ -f "backend/.env.example" ]; then
        cp backend/.env.example backend/.env
        echo "✅ Fichier .env créé."
    else
        echo "⚠️  Aucun fichier .env.example trouvé."
    fi
else
    echo "✅ Fichier .env déjà présent."
fi

echo

# =====================================================
# Lancement de l'application
# =====================================================

echo "[6/6] Démarrage du serveur Flask..."
echo
echo "======================================================"
echo "✅ Application prête !"
echo
echo "🌐 URL : http://localhost:5000"
echo
echo "⏹️  Arrêt : CTRL+C"
echo "======================================================"
echo

cd backend

python run.py