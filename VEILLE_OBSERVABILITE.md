Mission 1 : Comprendre PromQL
1. Quelle est la différence entre rate() et increase() ?

Les deux fonctions traitent des Counters mais elles expriment le résultat différemment. 
    
    rate() : Calcule l'augmentation moyenne par seconde sur l'intervalle de temps choisi, c'est l'outil principal pour mesurer le débit ou la charge.

    increase() : Calcule l'augmentation totale sur l'intervalle de temps. C'est plus parlant pour un humain : "Combien de requêtes avons-nous reçues durant la dernière heure ?".

2. Comment filtrer des métriques par label ?

On utilise des accolades {} immédiatement après le nom de la métrique avec des opérateurs :

    Égalité (=) : http_requests_total{status="200"}

    Inégalité (!=) : http_requests_total{status!="500"}

    in (=~) : http_requests_total{method=~"GET|POST"} (pour filtrer plusieurs valeurs).

    out (!~) : http_requests_total{job!~"node-.*"}

3. Que fait la fonction histogram_quantile() ?

Cette fonction est utilisée exclusivement avec les métriques de type Histogram. Elle permet de calculer des percentiles à partir des buckets collectés.

    Exemple : histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))

    Traduction : "Donne-moi le temps de réponse maximum pour 95% des utilisateurs sur les 5 dernières minutes."

Mission 2 : Best Practices Prometheus & Grafana
1. Comment nommer correctement une métrique ?

Selon les standards Prometheus :

    Suffixe d'unité : Le nom doit contenir l'unité au pluriel (ex: _seconds, _bytes, _total).

    Structure : On utilise le format domaine_objet_unité.

        Correct : http_request_duration_seconds

        Incorrect : request_time (on ne sait pas si c'est des ms ou des s).

    Le cas du Counter : Tout Counter doit obligatoirement se terminer par _total.

2. Quand utiliser des labels vs créer plusieurs métriques ?

    Utilisez des labels pour les caractéristiques d'une même métrique (ex: http_requests_total avec les labels method="GET" ou method="POST"). Cela permet de faire des sommes et des moyennes facilement.

    Créez des métriques distinctes si les choses mesurées sont de nature différente.

    ⚠️ Attention à la Cardinalité : Ne mettez jamais de données uniques dans un label (ID utilisateur, adresse email, timestamp). Cela créerait des millions de séries temporelles et ferait planter votre serveur Prometheus.

3. Quels sont les dashboards anti-patterns à éviter ?

    Le "Kitchen Sink" (Tout-en-un) : Mettre trop de graphiques sur une seule page. Un dashboard doit répondre à une intention précise.

    Manque de contexte : Ne pas mettre d'unités sur les axes Y (on ne sait pas si c'est des % ou des Go).

    Abus de couleurs : Utiliser des couleurs vives partout. Le rouge doit être réservé uniquement aux erreurs ou aux dépassements de seuils critiques.

    Requêtes trop lourdes : Faire des calculs complexes sur des périodes de temps géantes (ex: rate sur 30 jours) ce qui ralentit l'affichage du dashboard.