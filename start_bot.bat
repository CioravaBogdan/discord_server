@echo off
echo Restarting Discord Bot...
echo.

echo Opresc procesele existente...
taskkill /F /IM py.exe 2>nul
timeout /t 2 /nobreak >nul

echo Pornesc bot-ul...
start /B py main.py

echo.
echo Bot pornit! Verifica logs-urile.
echo Apasa orice tasta pentru a inchide...
pause >nul
