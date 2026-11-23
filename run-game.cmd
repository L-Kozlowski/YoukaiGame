@echo off
setlocal
if not exist "%~dp0.venv\Scripts\python.exe" (
    echo Brak srodowiska .venv. Najpierw zainstaluj zaleznosci gry.
    exit /b 1
)
pushd "%~dp0youkai"
"%~dp0.venv\Scripts\python.exe" -B menu.py
set "gameExitCode=%errorlevel%"
popd
exit /b %gameExitCode%
