@echo off
if "%~1"=="" (set name="db-temperature-distribution") else (set name="%~1")
for %%a in ("%cd%") do set "root=%%~dpa"
set pyexe=%root%.venv\Scripts\pyinstaller.exe
set dist=%root%dist
set build=%root%build
%pyexe% %root%main.py --onefile --name %name% --distpath %dist% --workpath %build% --specpath %root% --clean


