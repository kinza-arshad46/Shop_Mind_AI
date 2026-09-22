@echo off
echo Starting ShopMind AI...
start cmd /k "cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000"
timeout /t 3
streamlit run streamlit_app.py --server.port 8501
