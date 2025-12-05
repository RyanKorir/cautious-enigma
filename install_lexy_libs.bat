@echo off
title Lexy AI Butler Installer
echo ============================================
echo       Lexy AI Butler Full Installer
echo ============================================
echo.

REM ------------------------------
REM Check if Python is installed
REM ------------------------------
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python 3.8+ and rerun this script.
    pause
    exit /b
)
echo Python detected.

REM ------------------------------
REM Check if pip is installed
REM ------------------------------
python -m pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo pip not found. Installing pip...
    python -m ensurepip --upgrade
)
echo pip is installed.

REM ------------------------------
REM Upgrade pip
REM ------------------------------
echo Upgrading pip...
python -m pip install --upgrade pip

REM ------------------------------
REM Install required libraries
REM ------------------------------
echo Installing required Python libraries...
pip install --upgrade pyttsx3
pip install --upgrade plyer
pip install --upgrade dateparser
pip install --upgrade requests
pip install --upgrade beautifulsoup4
pip install --upgrade gensim
pip install --upgrade textblob
pip install --upgrade transformers
pip install --upgrade torch
pip install --upgrade speechrecognition
pip install --upgrade pyaudio
pip install --upgrade openai

REM ------------------------------
REM Download TextBlob corpora
REM ------------------------------
echo Downloading TextBlob corpora...
python -m textblob.download_corpora

echo.
echo ============================================
echo ✅ Lexy AI Butler is fully installed!
echo You can now run main.py to launch Lexy.
echo ============================================
pause
exit /b