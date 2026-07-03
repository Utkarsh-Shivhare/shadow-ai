# Quick Start Guide

## Prerequisites
- Python 3.9+
- Node.js 18+
- (Optional) GCP account with service account credentials

## Installation

### Backend Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
cd ..
```

## Configuration

Create a `.env` file or use the provided `.env.example`:

```bash
# For mock mode (no GCP needed)
USE_MOCK_GCP=true
GCP_PROJECT_ID=mock-shadow-ai-project

# For real GCP
# USE_MOCK_GCP=false
# GCP_PROJECT_ID=your-project-id
# GOOGLE_APPLICATION_CREDENTIALS=./credentials/service-account.json
```

## Running the Application

### Quick Start (Both Servers)
```bash
./start.sh
```

### Manual Start

**Terminal 1 - Backend:**
```bash
source venv/bin/activate
python -m backend.main
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Access

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Using the Application

1. Open http://localhost:5173
2. Click "Scan Project" to discover resources
3. View assets in the Assets tab
4. View detected AI agents in the Agents tab
5. Click any agent for detailed analysis

## Testing

### API Testing
```bash
# Health check
curl http://localhost:8000/

# List all agents
curl http://localhost:8000/agents

# Trigger scan
curl -X POST http://localhost:8000/scan

# Get statistics
curl http://localhost:8000/stats
```

## Troubleshooting

**Backend won't start:**
- Check port 8000 is available
- Verify virtual environment is activated
- Check dependencies: `pip list`

**Frontend won't start:**
- Check port 5173 is available
- Try deleting `node_modules` and run `npm install` again
- Verify Node.js version: `node --version` (should be 18+)

**No data showing:**
- Wait 2-3 seconds after triggering scan
- Check backend is running: `curl http://localhost:8000/`
- Verify `.env` configuration
