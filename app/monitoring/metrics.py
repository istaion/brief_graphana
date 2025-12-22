"""
Module de métriques Prometheus pour l'API Items
===============================================

Ce module définit toutes les métriques personnalisées utilisées pour
monitorer l'application FastAPI.

Types de métriques :
- Counter : Compteurs qui ne font qu'augmenter (ex: nombre de requêtes)
- Gauge : Valeurs qui peuvent monter et descendre (ex: connexions actives)
- Histogram : Distribution de valeurs avec buckets (ex: latences)
- Info : Informations statiques sur l'application
"""

from prometheus_client import Counter, Histogram, Gauge, Info
import time


# ============================================================================
# INFO : Informations statiques sur l'application
# ============================================================================

app_info = Info(
    'fastapi_app_info',
    'Information about the FastAPI application'
)


# ============================================================================
# COUNTER : Compteurs pour les opérations CRUD
# ============================================================================
# Les Counters ne font qu'augmenter et sont remis à zéro au redémarrage
# Utilisez rate() dans PromQL pour obtenir un taux par seconde

items_created_total = Counter(
    'items_created_total',
    'Nombre total d\'items créés depuis le démarrage de l\'application'
)

items_read_total = Counter(
    'items_read_total',
    'Nombre total de lectures d\'items (liste et détail)'
)

items_updated_total = Counter(
    'items_updated_total',
    'Nombre total d\'items mis à jour'
)

items_deleted_total = Counter(
    'items_deleted_total',
    'Nombre total d\'items supprimés'
)


# ============================================================================
# GAUGE : Valeurs instantanées
# ============================================================================
# Les Gauges peuvent monter et descendre - elles représentent une mesure instantanée

db_connection_pool_size = Gauge(
    'db_connection_pool_size',
    'Taille actuelle du pool de connexions à la base de données'
)

active_db_connections = Gauge(
    'active_db_connections',
    'Nombre de connexions actives à la base de données'
)


# ============================================================================
# HISTOGRAM : Distribution de valeurs avec buckets
# ============================================================================
# Les Histograms stockent les valeurs dans des buckets pour calculer des percentiles

db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Durée des requêtes à la base de données (en secondes)',
    # Buckets : de 1ms à 5 secondes
    # Adapté pour détecter les requêtes lentes
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)


# ============================================================================
# MÉTRIQUES CUSTOM BUSINESS
# ============================================================================
# Métrique personnalisée pour le domaine métier de l'application

items_total_value = Gauge(
    'items_total_value',
    'Valeur totale de tous les items en base (somme des prix)'
)


# ============================================================================
# CONTEXT MANAGER : Pour mesurer automatiquement les durées
# ============================================================================

class DatabaseQueryTimer:
    """
    Context manager pour mesurer automatiquement le temps d'exécution d'une requête DB.

    Utilisation :
        with DatabaseQueryTimer():
            # Code de la requête DB
            result = db.query(Item).all()

    La durée sera automatiquement enregistrée dans l'histogram db_query_duration_seconds.
    """

    def __enter__(self):
        """Enregistre le temps de début lors de l'entrée dans le contexte."""
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Calcule et enregistre la durée lors de la sortie du contexte.

        La durée est enregistrée même si une exception se produit.
        """
        duration = time.time() - self.start_time
        db_query_duration_seconds.observe(duration)
        # Ne pas supprimer l'exception (retourne None implicitement)
        return False
