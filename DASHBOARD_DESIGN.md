# Dashboard Design - Phase 3b

## Vue d'ensemble
Dashboard pour le monitoring de l'API Items.

## Layout
- 2 rangées de 3 panels
- Disposition optimisée pour une vue d'ensemble rapide

## Panels

### Rangée 1 - Opérations CRUD

#### 1. Items Créés Total
- **Type**: Stat
- **Métrique**: `items_created_total`
- **Description**: Nombre total d'items créés

#### 2. Opérations CRUD
- **Type**: Graph (Time series)
- **Métriques**:
  - `rate(items_created_total[5m])`
  - `rate(items_read_total[5m])`
  - `rate(items_updated_total[5m])`
  - `rate(items_deleted_total[5m])`
- **Description**: Taux d'opérations CRUD par seconde

#### 3. Distribution des Opérations
- **Type**: Pie Chart
- **Métriques**:
  - `items_created_total`
  - `items_read_total`
  - `items_updated_total`
  - `items_deleted_total`
- **Description**: Répartition des types d'opérations

### Rangée 2 - Performance Base de Données

#### 4. Durée des Requêtes DB
- **Type**: Graph (Time series)
- **Métriques**:
  - `histogram_quantile(0.95, rate(db_query_duration_seconds_bucket[5m]))`
  - `histogram_quantile(0.50, rate(db_query_duration_seconds_bucket[5m]))`
  - `rate(db_query_duration_seconds_sum[5m]) / rate(db_query_duration_seconds_count[5m])` (moyenne)
- **Description**: Percentiles (P95, P50) et temps moyen des requêtes DB

#### 5. Connexions DB Actives
- **Type**: Stat + Graph
- **Métrique**: `active_db_connections`
- **Description**: Nombre de connexions actives à la base de données

#### 6. Pool de Connexions
- **Type**: Gauge
- **Métrique**: `db_connection_pool_size`
- **Description**: Taille du pool de connexions DB

## Timerange
- Par défaut: Dernières 6 heures
- Refresh: 30s
