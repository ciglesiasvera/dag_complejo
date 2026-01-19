(myenv) cigle@DESKTOP-FQNJSRL:~/dag_complejo$ pytest -v tests/
=========================================================================================== test session starts ===========================================================================================platform linux -- Python 3.10.13, pytest-9.0.2, pluggy-1.6.0 -- /home/cigle/.pyenv/versions/3.10.13/bin/python3.10
cachedir: .pytest_cache
rootdir: /home/cigle/dag_complejo
plugins: time-machine-2.13.0, anyio-4.2.0
collected 3 items

tests/test_dag_complejo.py::TestDAGComplejo::test_dag_cargado PASSED                                                                                                                                [ 33%] 
tests/test_dag_complejo.py::TestDAGComplejo::test_dependencias_dag PASSED                                                                                                                           [ 66%] 
tests/test_dag_complejo.py::TestDAGComplejo::test_branching_logic PASSED                                                                                                                            [100%] 

============================================================================================ 3 passed in 0.88s ============================================================================================