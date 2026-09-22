.PHONY: install run backend frontend docker clean

install:
	pip install -r backend/requirements.txt
	pip install -r requirements.txt

backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend:
	streamlit run streamlit_app.py

run:
	@echo "Start backend in one terminal: make backend"
	@echo "Start frontend in another: make frontend"

docker:
	docker-compose up --build

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf backend/uploads/* backend/processed/* 2>/dev/null || true
