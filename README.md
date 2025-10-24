# Pinnote
DRF + React 개인 주식 관리 미니 프로젝트.

### Run
- Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt # 또는 위 명령대로 설치
python manage.py migrate
python manage.py runserver

diff
코드 복사
- Frontend
cd frontend
npm i
npm run dev

swift
코드 복사

### API
- GET /api/holdings/
- GET /api/holdings/summary/
- CRUD /api/stocks/, /api/trades/, /api/prices/ote" 
