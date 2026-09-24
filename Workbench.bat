@echo off
rem CanonSim Workbench - the ZERO-COMMAND launcher.
rem Double-click me: the gateway + the Redot frontend start together.
rem The Redot folder is asked for ONCE (a folder picker), then
rem remembered in workbench\runtime\launcher.json - no commands, ever.
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel%==0 goto :run
where py >nul 2>nul
if %errorlevel%==0 goto :runpy
echo Python was not found on PATH.
echo Install Python 3.11+ from python.org and check
echo "Add python.exe to PATH" in its installer, then run me again.
pause
exit /b 1
:run
python scripts\workbench_launch.py %*
goto :end
:runpy
py -3 scripts\workbench_launch.py %*
goto :end
:end
if errorlevel 1 pause
endlocal
