"""Configuration de la base de données et gestion des sessions.

Ce module gère la connexion à la base de données PostgreSQL
et fournit une fonction générateur pour obtenir des sessions de base de données.
"""

import os
from dotenv import load_dotenv
from sqlmodel import Session, create_engine

# Charger les variables d'environnement depuis .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

POOL_SIZE = 10

engine = create_engine(DATABASE_URL)


def get_db():
    with Session(engine) as session:
        yield session
