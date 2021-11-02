call build.bat "db-temperature-distribution 0.1.0"
for %%a in ("%cd%") do set "root=%%~dpa"
set pytestexe=%root%.venv\Scripts\pytest.exe
%pytestexe% %root%tests/test_executable.py
