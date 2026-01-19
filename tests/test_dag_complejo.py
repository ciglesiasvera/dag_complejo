def test_branching_logic(self):
        """
        Test unitario de la función Python pura.
        Simulamos (Mock) el contexto de Airflow.
        """
        # 1. Crear un Mock para el TaskInstance (TI)
        mock_ti = MagicMock()
        
        # 2. Crear un diccionario REAL para el contexto
        # Esto es crucial: **context espera un dict, no un MagicMock directo
        contexto_simulado = {
            'task_instance': mock_ti
        }

        # --- Caso A: Calidad Alta ---
        # Configuramos el comportamiento del mock
        mock_ti.xcom_pull.return_value = 'alta'
        
        # Pasamos el diccionario desempaquetado
        resultado = decidir_procesamiento(**contexto_simulado)
        assert resultado == 'procesamiento_rapido'

        # --- Caso B: Calidad Baja ---
        mock_ti.xcom_pull.return_value = 'baja' # Cambiamos el valor simulado
        
        resultado = decidir_procesamiento(**contexto_simulado)
        assert resultado == 'procesamiento_completo'