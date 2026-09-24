@echo off
rem CanonSim Workbench Setup - re-pick the Redot folder.
rem Opens the folder picker once (pick the folder that contains
rem redot.windows.editor.x86_64.exe); the pick is remembered and the
rem Workbench starts immediately with it.
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
python scripts\workbench_launch.py --pick-redot %*
goto :end
:runpy
py -3 scripts\workbench_launch.py --pick-redot %*
goto :end
:end
if errorlevel 1 pause
endlocal
