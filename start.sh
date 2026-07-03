#!/bin/bash

# Shadow AI Discovery Engine - Quick Start Script

echo "🚀 Starting Shadow AI Discovery Engine..."
echo ""

# Colors for output
GREEN='\033[0.32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install backend dependencies if needed
if [ ! -f "venv/bin/uvicorn" ]; then
    echo "${YELLOW}Installing backend dependencies...${NC}"
    pip install -r backend/requirements.txt
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "${YELLOW}Installing frontend dependencies...${NC}"
    cd frontend
    npm install
    cd ..
fi

echo ""
echo "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Start backend in background
echo "${YELLOW}Starting backend server on http://localhost:8000...${NC}"
python -m backend.main &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start frontend
echo "${YELLOW}Starting frontend server on http://localhost:5173...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "${GREEN}✓ Shadow AI Discovery Engine is running!${NC}"
echo ""
echo "  Backend API:  http://localhost:8000"
echo "  Frontend UI:  http://localhost:5173"
echo "  API Docs:     http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for user to press Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
