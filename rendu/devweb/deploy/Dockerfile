FROM python:3.11-slim

# Comportement Python adapté aux conteneurs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    FLASK_APP=run.py

WORKDIR /app/backend

# Dépendances système minimales (curl pour le HEALTHCHECK,
# build-essential au cas où une dépendance Python nécessite une compilation)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python (étape mise en cache séparément du code)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le backend, puis le frontend (templates/static référencés en chemin relatif)
COPY backend/ .
COPY frontend/ /app/frontend

# Dossier instance (SQLite) + logs : créés et rendus accessibles à un user non-root
RUN mkdir -p instance logs

# Utilisateur non-root
RUN useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "60", "run:app"]