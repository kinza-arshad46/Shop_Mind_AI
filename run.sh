#!/bin/bash
# ShopMind AI - Quick Launch Script

echo "🧠 Starting ShopMind AI..."
echo ""

# Check if backend deps are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing backend dependencies..."
    pip install -r backend/requirements.txt
fi

if ! python -c "import streamlit" 2>/dev/null; then
    echo "📦 Installing frontend dependencies..."
    pip install -r requirements.txt
fi

# Start backend in background
echo "🚀 Starting FastAPI backend on port 8000..."
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait for backend
sleep 3

# Start frontend
echo "🎨 Starting Streamlit frontend on port 8501..."
echo ""
echo "✅ Open http://localhost:8501 in your browser"
echo "📚 API docs: http://localhost:8000/docs"
echo ""
streamlit run streamlit_app.py --server.port 8501

# Cleanup
kill $BACKEND_PID 2>/dev/null
