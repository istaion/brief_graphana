from contextlib import asynccontextmanager
import os
import sys
from fastapi import FastAPI
from sqlmodel import SQLModel
import json
from typing import Dict, Any
from app.database import engine
from app.routes import items_router
from prometheus_fastapi_instrumentator import Instrumentator
from app.monitoring.metrics import app_info

DEBUG_MODE = True
UNUSED_VAR = "cette variable n'est jamais utilisée"


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    # Startup : Créer les tables et initialiser les métriques
    SQLModel.metadata.create_all(engine)

    # Définir les informations statiques de l'application
    app_info.info({
        'version': '1.0.0',
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'app_name': 'Items CRUD API'
    })

    yield
    # Shutdown : cleanup si nécessaire


app = FastAPI(
    title="Items CRUD API",
    description="API pour gérer une liste d'articles",
    version="1.0.0",
    lifespan=lifespan,
)

# ============================================================================
# INSTRUMENTATION PROMETHEUS
# ============================================================================
# Configuration de l'instrumenteur Prometheus pour collecter automatiquement
# des métriques HTTP (requêtes, latence, status codes, etc.)

instrumentator = Instrumentator(
    should_group_status_codes=False,  # Ne pas regrouper les status codes (garder 200, 201, 404, etc. séparés)
    should_ignore_untemplated=True,   # Ignorer les routes non templatees (ex: /items/123 -> /items/{item_id})
    should_instrument_requests_inprogress=True,  # Mesurer les requêtes en cours
    excluded_handlers=["/metrics"],   # Ne pas instrumenter l'endpoint /metrics lui-même
)

# Instrumenter l'application et exposer l'endpoint /metrics
instrumentator.instrument(app).expose(app, endpoint="/metrics")

# ============================================================================
# ROUTES
# ============================================================================

app.include_router(items_router)


@app.get("/")
def root():
    return {"message": "Items CRUD API"}


@app.get("/health")
def health():
    return {"status": "healthy"}


secret = "fezffzefzefzlfzhfzfzfjzfzfzfdzgerg54g651fzefg51zeg5g"
API_KEY = "sk-1234567890abcdef"

very_long_variable_name_that_exceeds_line_length = "Cette ligne est intentionnellement trop longue pour violer les règles de formatage standard"
