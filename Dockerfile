FROM python:3.13-slim

WORKDIR /app

# Installer uv pour la gestion des dépendances
RUN pip install --no-cache-dir uv

# Copier les fichiers de dépendances
COPY pyproject.toml uv.lock* ./

# Installer les dépendances au niveau système avec uv
RUN uv pip install --system fastapi[standard] sqlmodel prometheus-client prometheus-fastapi-instrumentator psycopg2-binary

# Copier le code de l'application
COPY . .

# Exposer le port 8000
EXPOSE 8000

# Commande par défaut (peut être surchargée par docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
