"""Configuration de la base de données et gestion des sessions.

Ce module gère la connexion à la base de données PostgreSQL
et fournit une fonction générateur pour obtenir des sessions de base de données.
"""

import os
from dotenv import load_dotenv
from sqlmodel import Session, create_engine
from app.monitoring.metrics import db_connection_pool_size, active_db_connections

# Charger les variables d'environnement depuis .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

POOL_SIZE = 10

engine = create_engine(DATABASE_URL, pool_size=POOL_SIZE, max_overflow=20)

# Initialiser la métrique du pool size
db_connection_pool_size.set(POOL_SIZE)


def get_db():
    with Session(engine) as session:
        # Incrémenter le compteur de connexions actives
        active_db_connections.inc()
        try:
            yield session
        finally:
            # Décrémenter le compteur de connexions actives
            active_db_connections.dec()
