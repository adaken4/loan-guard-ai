#!/bin/bash

echo "🛡️  LoanGuard AI - Quick Start Script"
echo "======================================"

# Check if virtual environment exists
if [ ! -d "loan_guard_venv" ]; then
    echo "❌ Virtual environment not found. Creating..."
    python3 -m venv loan_guard_venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source laon_guard_venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -q -r requirements.txt

# Train model if not exists
if [ ! -f "model/risk_model.pkl" ]; then
    echo "🧠 Training ML model..."
    python -m model.train_model
else
    echo "✅ Model already trained"
fi

# Start backend
echo "🚀 Starting FastAPI backend on port 8000..."
uvicorn api.main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

echo ""
echo "✅ Backend running at http://localhost:8000"
echo "📚 API docs at http://localhost:8000/docs"
echo ""
echo "To start frontend:"
echo "  cd frontend"
echo "  npm install"
echo "  npm run dev"
echo ""
echo "Press Ctrl+C to stop backend"

# Wait for user interrupt
wait $BACKEND_PID
