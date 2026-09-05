#!/usr/bin/env bash
# Start the full SETU-STAT demo stack: backend (8001) + frontend (8090)
cd "$(dirname "$0")"
pkill -f "uvicorn main:app" 2>/dev/null
cd backend && (setsid nohup python3 -m uvicorn main:app --port 8001 > /tmp/igot-backend.log 2>&1 < /dev/null &)
cd ../dummy-igot && (setsid nohup python3 -m http.server 8090 > /tmp/igot-frontend.log 2>&1 < /dev/null &)
sleep 6
echo "frontend: http://localhost:8090"
curl -s http://localhost:8001/api/health
