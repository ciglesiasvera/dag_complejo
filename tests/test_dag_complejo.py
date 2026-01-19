import pytest
import os
from airflow.models import DagBag
from unittest.mock import MagicMock

# Importamos las funciones reales del DAG para probar su lógica
# Nota: Asegúrate de que Python pueda encontrar el módulo 'dags'
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../dags'))
from pipeline_complejo import decidir_procesamiento

class TestDAGComplejo:
    
    @pytest.fixture
    def dagbag(self):
        """
        Carga los DAGs para testing.
        Usa os.path para encontrar la carpeta 'dags' relativa a este archivo de test.
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dag_folder = os.path.join(base_dir, 'dags')
        
        # include_examples=False para que no cargue los DAGs de ejemplo de Airflow y sea más rápido
        return DagBag(dag_folder=dag_folder, include_examples=False)
    
    def test_dag_cargado(self, dagbag):
        """Verificar que el DAG no tiene errores de importación y existe"""
        # Verificar que no hubo errores generales al importar (SyntaxErrors, etc.)
        assert len(dagbag.import_errors) == 0, f"Errores de importación: {dagbag.import_errors}"
        
        dag = dagbag.get_dag('pipeline_avanzado_complejo')
        assert dag is not None
        assert len(dag.tasks) >= 5 # Verificamos que tenga tareas
    
    def test_dependencias_dag(self, dagbag):
        """Verificar la estructura del grafo (Upstream/Downstream)"""
        dag = dagbag.get_dag('pipeline_avanzado_complejo')
        
        # Verificar tarea inicial
        inicio = dag.get_task('inicio')
        # La tarea inicio no debe tener padres (upstream)
        assert len(inicio.upstream_task_ids) == 0
        
        # Verificar tarea final
        fin = dag.get_task('fin')
        # La tarea fin no debe tener hijos (downstream)
        assert len(fin.downstream_task_ids) == 0
        
        # Verificar que 'union_rutas' depende del TaskGroup y las ramas
        union = dag.get_task('union_rutas')
        assert 'procesamiento_pesado.paso3' in union.upstream_task_ids
        assert 'procesamiento_rapido' in union.upstream_task_ids

    def test_branching_logic(self):
        """
        Test unitario de la función Python pura.
        Simulamos (Mock) el contexto de Airflow.
        """
        # 1. Crear un Mock para el 'task_instance' y xcom_pull
        mock_context = MagicMock()
        mock_ti = MagicMock()
        
        # Caso A: Calidad Alta
        mock_ti.xcom_pull.return_value = 'alta'
        mock_context['task_instance'] = mock_ti
        
        resultado = decidir_procesamiento(**mock_context)
        assert resultado == 'procesamiento_rapido'

        # Caso B: Calidad Baja
        mock_ti.xcom_pull.return_value = 'baja' # Cambiamos el valor simulado
        
        resultado = decidir_procesamiento(**mock_context)
        assert resultado == 'procesamiento_completo'