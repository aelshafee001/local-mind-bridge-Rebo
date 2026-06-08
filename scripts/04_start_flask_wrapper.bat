@echo off
cd /d %~dp0\..\flask_wrapper
pip install -r requirements.txt
python app.py
pause
