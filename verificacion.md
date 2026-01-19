Respuestas a la verificación

Pregunta 1: ¿Cuándo usar SubDAGs vs TaskGroups?

- SubDAGs: útiles cuando se necesita que un conjunto de tareas tenga su propio programador, retries y lógica independiente, casi como un DAG dentro de otro. Se recomienda cuando el bloque de tareas es muy complejo y puede ejecutarse de forma autónoma.

- TaskGroups: ideales para organizar visualmente y agrupar tareas en la UI de Airflow, sin afectar la ejecución ni la lógica de scheduling. Es más ligero y recomendado para la mayoría de casos.

Pregunta 2: Estrategias de escalado efectivas según la carga de trabajo

- Tareas ligeras y frecuentes: usar concurrency control y TaskGroups, escalar con más workers y un scheduler eficiente.

- Tareas pesadas o batch: considerar SubDAGs o DAGs separados para aislar la ejecución, usar parallelización y pools, y recursos dedicados de workers.

- Datos muy grandes: integrar con cluster de procesamiento externo (Spark, KubernetesPodOperator) y balancear la carga entre workers.

