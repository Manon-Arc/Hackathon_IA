@echo off
setlocal

title Assistant Financier - Demarrage

echo.
echo ======================================================
echo        ASSISTANT FINANCIER - DEMARRAGE
echo ======================================================
echo.

REM ======================================================
REM Se placer a la racine du projet
REM ======================================================

cd /d "%~dp0.."

echo [INFO] Repertoire du projet :
echo        %CD%
echo.

REM ======================================================
REM Verification de Python
REM ======================================================

echo [1/6] Verification de Python...

python --version >nul 2>&1

if errorlevel 1 (
    echo.
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH.
    echo.
    pause
    exit /b 1
)

python --version
echo.

REM ======================================================
REM Creation de l'environnement virtuel
REM ======================================================

echo [2/6] Verification de l'environnement virtuel...

if not exist "venv" (
    echo.
    echo    -> Creation du venv...
    python -m venv venv

    if errorlevel 1 (
        echo.
        echo [ERREUR] Impossible de creer l'environnement virtuel.
        pause
        exit /b 1
    )

    echo    -> Venv cree avec succes.
) else (
    echo    -> Venv deja present.
)

echo.

REM ======================================================
REM Activation
REM ======================================================

echo [3/6] Activation du venv...

call venv\Scripts\activate.bat

if errorlevel 1 (
    echo.
    echo [ERREUR] Impossible d'activer le venv.
    pause
    exit /b 1
)

echo    -> Venv active.
echo.

REM ======================================================
REM Installation des dependances
REM ======================================================

echo [4/6] Installation / Mise a jour des dependances...

python -m pip install --upgrade pip

pip install -r backend\requirements.txt

if errorlevel 1 (
    echo.
    echo [ERREUR] L'installation des dependances a echoue.
    pause
    exit /b 1
)

echo    -> Dependances OK.
echo.

REM ======================================================
REM Configuration
REM ======================================================

echo [5/6] Verification du fichier .env...

if not exist "backend\.env" (
    if exist "backend\.env.example" (
        copy "backend\.env.example" "backend\.env" >nul
        echo    -> Fichier .env cree.
    ) else (
        echo    -> Aucun .env.example trouve.
    )
) else (
    echo    -> Fichier .env deja present.
)

echo.

REM ======================================================
REM Lancement
REM ======================================================

echo [6/6] Demarrage du serveur Flask...
echo.
echo ======================================================
echo Application disponible sur :
echo.
echo    http://localhost:5000
echo.
echo Pour arreter :
echo    CTRL + C
echo ======================================================
echo.

cd backend

python run.py

echo.
echo ======================================================
echo Le serveur est arrete.
echo ======================================================
echo.

pause