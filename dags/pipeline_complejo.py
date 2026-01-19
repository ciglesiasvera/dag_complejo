from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator 
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
import random

# -----------------------------
# Funciones de las tareas
# -----------------------------
def validar_calidad_datos(**context):
    """Simula la validación de calidad de datos"""
    calidad = random.choice(['alta', 'media', 'baja'])
    context['task_instance'].xcom_push(key='calidad', value=calidad)
    print(f"Calidad de datos: {calidad}")
    return calidad

def decidir_procesamiento(**context):
    """Decide la ruta de procesamiento según la calidad"""
    calidad = context['task_instance'].xcom_pull(task_ids='validar_calidad', key='calidad')
    if calidad == 'alta':
        print("Ruta: procesamiento rápido")
        return 'procesamiento_rapido'
    else:
        print("Ruta: procesamiento completo")
        return 'procesamiento_completo'

def procesamiento_rapido():
    print("Ejecutando procesamiento optimizado para datos de alta calidad")

def procesamiento_completo():
    print("Ejecutando procesamiento completo con validaciones adicionales")

# -----------------------------
# DAG completo usando context manager
# -----------------------------
with DAG(
    dag_id='pipeline_avanzado_complejo',
    description='Pipeline con patrones avanzados: branching, TaskGroup y XCom',
    schedule='@daily',  # CORRECCIÓN: 'schedule' en lugar de 'schedule_interval' (Airflow 2.4+)
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={
        'retries': 2,
        'retry_delay': timedelta(minutes=5),
        'execution_timeout': timedelta(hours=1)
    }
) as dag:

    # -----------------------------
    # Tareas externas
    # -----------------------------
    # CORRECCIÓN: Usamos EmptyOperator
    inicio = EmptyOperator(task_id='inicio', dag=dag)
    
    validar = PythonOperator(
        task_id='validar_calidad',
        python_callable=validar_calidad_datos,
        # provide_context=True,  <-- Eliminado porque ya no es necesario en Airflow 2.0+
        dag=dag
    )
    decidir = BranchPythonOperator(
        task_id='decidir_ruta',
        python_callable=decidir_procesamiento,
        # provide_context=True,  <-- Eliminado
        dag=dag
    )
    ruta_rapida = PythonOperator(
        task_id='procesamiento_rapido',
        python_callable=procesamiento_rapido,
        dag=dag
    )
    ruta_completa = PythonOperator(
        task_id='procesamiento_completo',
        python_callable=procesamiento_completo,
        dag=dag
    )

    # -----------------------------
    # TaskGroup para procesamiento pesado
    # -----------------------------
    with TaskGroup('procesamiento_pesado', dag=dag) as procesamiento_group:
        paso1 = PythonOperator(task_id='paso1', python_callable=lambda: print("Paso 1"))
        paso2 = PythonOperator(task_id='paso2', python_callable=lambda: print("Paso 2"))
        paso3 = PythonOperator(task_id='paso3', python_callable=lambda: print("Paso 3"))

        # Dependencias internas del TaskGroup
        paso1 >> paso2 >> paso3

    # -----------------------------
    # Unión y finalización
    # -----------------------------
    # CORRECCIÓN: Usamos EmptyOperator
    union = EmptyOperator(
        task_id='union_rutas', 
        dag=dag, 
        trigger_rule='one_success' # Importante para branching
    )
    
    fin = EmptyOperator(task_id='fin', dag=dag)

    # -----------------------------
    # Flujo principal
    # -----------------------------
    inicio >> validar >> decidir
    
    # Definición de ramas y conexión con el grupo
    decidir >> [ruta_rapida, ruta_completa, procesamiento_group]
    
    # Convergencia
    [ruta_rapida, ruta_completa, procesamiento_group] >> union >> fin