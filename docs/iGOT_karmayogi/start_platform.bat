@echo off
echo ======================================================================
echo Starting MoSPI iGOT Karmayogi AI Skill Intelligence Platform
echo ======================================================================

echo [1/2] Launching FastAPI Backend on http://127.0.0.1:8000 ...
start "MoSPI Backend (FastAPI)" cmd /k "cd /d %~dp0backend && python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"

echo [2/2] Launching Frontend on http://localhost:5173 ...
start "MoSPI Frontend (Vite React)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ======================================================================
echo Platform is online!
echo Frontend: http://localhost:5173
echo Backend API Docs: http://127.0.0.1:8000/docs
echo ======================================================================
pause
