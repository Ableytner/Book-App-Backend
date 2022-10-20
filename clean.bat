@echo off
FOR /d /r . %%d IN (__pycache__, .pytest_cache) DO @IF EXIST "%%d" rd /s /q "%%d"
IF EXIST .\bookappbackend\tests\test.db del .\bookappbackend\tests\test.db
IF EXIST .\bookappbackend\database\database.db del .\bookappbackend\database\database.db
