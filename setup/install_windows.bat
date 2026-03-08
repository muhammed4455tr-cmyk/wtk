@echo off
setlocal

where python >nul 2>nul
if %errorlevel% neq 0 (
  echo Python bulunamadi. Lutfen Python 3.11+ kurup tekrar deneyin.
  pause
  exit /b 1
)

python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python src\main.py

endlocal
