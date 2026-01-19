import pytest
import os
import sys
from airflow.models import DagBag
from unittest.mock import MagicMock

# -------------------------------------------------------------------------
# Configuración de Path
# -------------------------------------------------------------------------
# Agregamos la carpeta 'dags' al path de Python para poder importar 
# las funciones del DAG (necesario para el test unitario)
sys.path.append(os.path.join(os.path.dirname(__file__), '../dags'))

# Importamos la función específica a testear
from pipeline_complejo import decidir_procesamiento

class TestDAGComplejo:
    
    @pytest.fixture
    def dagbag(self):
        """
        Fixture que carga la colección de DAGs una sola vez por test.
        """
        # Calcula la ruta absoluta a la carpeta 'dags'
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dag_folder = os.path.join(base_dir, 'dags')
        
        # include_examples=False hace que la carga sea más rápida
        return DagBag(dag_folder=dag_folder, include_examples=False)
    
    def test_dag_cargado(self, dagbag):
        """
        Verifica que el DAG se carga sin errores de sintaxis.
        """
        # 1. Verificar que no existan errores de importación (sintaxis, librerías faltantes)
        assert len(dagbag.import_errors) == 0, f"Errores de importación encontrados: {dagbag.import_errors}"
        
        # 2. Obtener el DAG usando .dags.get()
        # IMPORTANTE: Usamos .dags.get('id') en lugar de .get_dag('id')
        # .dags es un diccionario en memoria. .get_dag() intenta consultar la DB (y falla si no hay DB).
        dag = dagbag.dags.get('pipeline_avanzado_complejo')
        
        # 3. Validaciones básicas
        assert dag is not None, "El DAG no se encontró en la memoria del DagBag"
        assert len(dag.tasks) >= 5, "El DAG debería tener al menos 5 tareas"
    
    def test_dependencias_dag(self, dagbag):
        """
        Verifica la estructura del grafo (dependencias Upstream/Downstream).
        """
        dag = dagbag.dags.get('pipeline_avanzado_complejo')
        assert dag is not None
        
        # A. Verificar tarea inicial
        inicio = dag.get_task('inicio')
        assert len(inicio.upstream_task_ids) == 0, "La tarea 'inicio' no debería tener padres"
        
        # B. Verificar tarea final
        fin = dag.get_task('fin')
        assert len(fin.downstream_task_ids) == 0, "La tarea 'fin' no debería tener hijos"
        
        # C. Verificar la tarea de Unión
        # Debe recibir conexiones de: ruta rápida, ruta completa y el final del TaskGroup
        union = dag.get_task('union_rutas')
        deps = union.upstream_task_ids
        
        assert 'procesamiento_rapido' in deps
        assert 'procesamiento_completo' in deps
        # Nota: En TaskGroups, la dependencia viene de la última tarea del grupo
        assert 'procesamiento_pesado.paso3' in deps

    def test_branching_logic(self):
        """
        Test Unitario puro de la función Python 'decidir_procesamiento'.
        Usa Mocks para simular Airflow sin necesitar base de datos.
        """
        # 1. Crear un Mock para simular 'task_instance'
        mock_ti = MagicMock()
        
        # 2. Crear el diccionario de contexto que espera la función (**kwargs)
        contexto_simulado = {
            'task_instance': mock_ti
        }

        # --- ESCENARIO 1: Calidad Alta ---
        # Simulamos que xcom_pull devuelve 'alta'
        mock_ti.xcom_pull.return_value = 'alta'
        
        # Ejecutamos la función real
        resultado = decidir_procesamiento(**contexto_simulado)
        
        # Verificamos que decida ir por la ruta rápida
        assert resultado == 'procesamiento_rapido'

        # --- ESCENARIO 2: Calidad Baja ---
        # Simulamos que xcom_pull devuelve 'baja'
        mock_ti.xcom_pull.return_value = 'baja' 
        
        # Ejecutamos la función real
        resultado = decidir_procesamiento(**contexto_simulado)
        
        # Verificamos que decida ir por la ruta completa
        assert resultado == 'procesamiento_completo'