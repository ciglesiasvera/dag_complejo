# DAG Complejo con Airflow: Pipeline Avanzado con Best Practices

## 📌 Objetivo del Proyecto

Este proyecto tiene como objetivo implementar un **DAG complejo en Apache Airflow** que integre patrones avanzados de diseño, incluyendo:

- Branching dinámico según la calidad de los datos.
- TaskGroups para agrupar tareas relacionadas.
- SubDAGs opcionales para bloques de tareas autónomos.
- Estrategias de escalado y buenas prácticas de configuración.
- Testing automatizado de DAGs.
- Integración de CI/CD usando GitHub Actions para asegurar la calidad del código antes de desplegar.

El propósito es **simular un pipeline de procesamiento de datos avanzado**, aplicando conceptos de ingeniería de datos y asegurando confiabilidad mediante pruebas y validación continua.

---

## 🛠 Estructura del Proyecto

```

dag_complejo/
├── dags/
│   └── pipeline_complejo.py
├── tests/
│   └── test_dag_complejo.py
├── .github/
│   └── workflows/
│       └── test-dags.yml
└── README.md

````

---

## ⚡ Requisitos Previos

- Python 3.8+
- Apache Airflow 2.8.1
- pytest
- Git y GitHub (para CI/CD)

---

## 🚀 Pasos para Construir el Proyecto

### 1. Crear la carpeta del proyecto y entorno virtual
```bash
mkdir dag_complejo
cd dag_complejo
python3 -m venv myenv
source myenv/bin/activate  # Linux / Mac
# myenv\Scripts\activate    # Windows
````

### 2. Instalar Airflow

```bash
pip install "apache-airflow[webserver]==2.8.1" Flask-Session
```

### 3. Crear carpetas para DAGs y tests

```bash
mkdir dags tests
```

### 4. Crear el DAG complejo

* Archivo: `dags/pipeline_complejo.py`
* Implementa:

  * DummyOperators de inicio y fin
  * PythonOperators para validación y procesamiento
  * BranchPythonOperator para rutas condicionales
  * TaskGroup para procesamiento pesado
  * Conexión y unión de rutas al final

**Conceptos aplicados:**

* XComs para compartir información entre tareas
* Branching dinámico
* TaskGroup para agrupar tareas complejas
* Best practices: retries, timeout, schedule diario, catchup desactivado

---

### 5. Implementar Testing

* Archivo: `tests/test_dag_complejo.py`
* Incluye tests para:

  * Carga correcta del DAG
  * Dependencias correctas (upstream/downstream)
  * Lógica de branching simulando contextos con `xcom_pull`
* Se utiliza **pytest** y fixtures para cargar DAGs

---

### 6. Configurar CI/CD con GitHub Actions

* Archivo: `.github/workflows/test-dags.yml`
* Funcionalidad:

  * Ejecutar tests automáticamente al hacer push en `dags/**`
  * Instalar Python y dependencias
  * Ejecutar `pytest` para tests
  * Validar sintaxis y carga de todos los DAGs con `DagBag`
* Garantiza que cualquier cambio que rompa el DAG sea detectado antes de desplegarlo

---

### 7. Configurar Airflow para usar el DAG del proyecto

1. Definir el **AIRFLOW_HOME** apuntando a la carpeta del proyecto:

```bash
export AIRFLOW_HOME=$(pwd)  # Linux / Mac
# set AIRFLOW_HOME=%cd%      # Windows PowerShell
```

2. Inicializar la base de datos de Airflow (crea tablas y estructura necesaria):

# Migrar la base de datos (crea tablas si no existen y aplica migraciones)
airflow db migrate

# Aplicar migraciones pendientes para asegurar esquema actualizado
airflow db upgrade

3. Crear usuario administrador:

```bash
airflow users create \
    --username admin \
    --firstname Cristian \
    --lastname Iglesias \
    --role Admin \
    --email admin@example.com
```

4. Iniciar Scheduler y Webserver:

```bash
# Scheduler: ejecuta tareas programadas
airflow scheduler

# Webserver: interfaz UI de Airflow
airflow webserver --port 8080
```

5. Abrir UI en el navegador:

```
http://localhost:8080
```

Se recomiendo configurar el proyecto sin proyectos de ejemplo para que no haya conflictos con los DAGs del proyecto.
en airflow.cfg se recomienda configurar: 

```
include_examples = False
```

El DAG `pipeline_avanzado_complejo` debería aparecer automáticamente, cargando desde `dag_complejo/dags/pipeline_complejo.py`.

---

## ✅ Resumen de Conceptos Aplicados

* **Branching dinámico:** decisiones según la calidad de los datos (`BranchPythonOperator`)
* **TaskGroup:** agrupa pasos complejos en un solo bloque visual
* **SubDAG (opcional):** útil para tareas independientes y escalables
* **Best Practices:** retries, timeout, catchup=False
* **Testing:** pytest, fixtures, pruebas unitarias y de dependencias
* **CI/CD:** GitHub Actions valida DAGs y tests automáticamente

---

## 💡 Buenas Prácticas

1. Usar TaskGroups para organizar DAGs visualmente.
2. Reservar SubDAGs para procesos autónomos y muy pesados.
3. Configurar retries y timeout para tareas críticas.
4. Versionar los DAGs con Git y validar cambios con CI/CD.
5. Mantener tests unitarios y de integración para detectar errores temprano.

---

## 📚 Referencias

* [Airflow Documentation](https://airflow.apache.org/docs/)
* [Airflow TaskGroup vs SubDAG](https://airflow.apache.org/docs/apache-airflow/stable/concepts.html#taskgroups)
* [pytest fixtures](https://docs.pytest.org/en/stable/fixture.html)
* [GitHub Actions for Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)


