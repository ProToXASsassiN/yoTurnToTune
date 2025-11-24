@echo off
echo ========================================
echo   yoTuneToTune PRO - Studio Edition
echo ========================================
echo.

REM Verification de Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERREUR: Python n'est pas installe!
    echo.
    echo Telechargez Python depuis: https://www.python.org/downloads/
    echo IMPORTANT: Cochez "Add Python to PATH" lors de l'installation!
    echo.
    pause
    exit /b 1
)

echo Python detecte!
echo.

REM Verification des dependances
echo Verification des dependances...
pip show numpy >nul 2>&1
if %errorlevel% neq 0 (
    echo Installation des dependances...
    pip install -r requirements.txt
    REM Verification que l'installation a reussi
    pip show numpy >nul 2>&1
    if %errorlevel% neq 0 (
        echo.
        echo ERREUR: Impossible d'installer les dependances!
        pause
        exit /b 1
    )
    echo Dependances installees avec succes!
) else (
    echo Dependances OK!
)

echo.
echo Demarrage de l'interface PRO...
echo.

REM Lance la version GUI
python gui_premium.py

if %errorlevel% neq 0 (
    echo.
    echo Le programme s'est termine avec une erreur.
    pause
)
