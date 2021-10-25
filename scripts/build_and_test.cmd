call build.bat db-temperature-distribution
for %%a in ("%cd%") do set "root=%%~dpa"
set pytestexe=%root%.venv\Scripts\pytest.exe
%pytestexe% %root%tests/test_package.py
