# Quick Start Guide

## Prerequisites
- Python 3.9+ installed
- Node.js 18+ and npm installed
- (Optional) GCP account with service account credentials

## Setup in 3 Steps

### 1. Install Dependencies

**Backend:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### 2. Configure Environment

The `.env` file is already configured for Mock mode (no GCP needed):
```env
USE_MOCK_GCP=true
GCP_PROJECT_ID=mock-shadow-ai-project
```

**To use real GCP later:**
1. Create a GCP project and service account
2. Download the JSON key to `credentials/gcp-service-account.json`
3. Update `.env`:
   ```env
   USE_MOCK_GCP=false
   GCP_PROJECT_ID=your-project-id
   GOOGLE_APPLICATION_CREDENTIALS=./credentials/gcp-service-account.json
   ```

### 3. Run the Application

**Option A: Quick Start (Both servers)**
```bash
./start.sh
```

**Option B: Manual Start**

Terminal 1 - Backend:
```bash
source venv/bin/activate
python -m backend.main
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

## Access the Application

- **Frontend UI:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs (FastAPI Swagger UI)

## First Steps

1. Open http://localhost:5173 in your browser
2. Click "Scan Project" on the Dashboard
3. Wait 2-3 seconds for the scan to complete
4. View discovered assets and AI agents
5. Click on any agent to see detailed analysis

## What You'll See

### Dashboard
- Total assets and AI agents detected
- Average confidence and risk scores
- Quick stats and actions

### Assets View
- All discovered cloud resources
- Filter by type (Cloud Run, Functions, GKE, Vertex AI)
- Resource metadata and labels

### Agents View
- Detected AI workloads in a table
- Confidence scores and risk assessment
- Click any row to see details

### Agent Details
- Complete confidence score breakdown
- Risk assessment with factors
- All detected indicators
- Environment variables (sensitive data masked)
- Full resource metadata

## Testing the API Directly

### Get all agents:
```bash
curl http://localhost:8000/agents | jq
```

### Get statistics:
```bash
curl http://localhost:8000/stats | jq
```

### Trigger a scan:
```bash
curl -X POST http://localhost:8000/scan
```

### Get specific agent details:
```bash
curl http://localhost:8000/agents/agent-cloud-run-001 | jq
```

## Mock Data

The mock mode includes realistic examples:
- **Cloud Run services:** ai-chatbot-service, document-processor, vertex-ai-pipeline
- **Cloud Functions:** intelligent-summarizer, embedding-generator
- **GKE workloads:** crewai-agents-deployment, autogen-studio
- **Vertex AI:** custom-llm-endpoint, gemini-pro-endpoint

All with varying confidence scores (70-100%) and risk levels (0-90).

## Troubleshooting

### Backend won't start
- Make sure port 8000 is not in use
- Check that virtual environment is activated
- Verify all dependencies are installed: `pip list`

### Frontend won't start
- Make sure port 5173 is not in use
- Delete `node_modules` and run `npm install` again
- Check Node.js version: `node --version` (should be 18+)

### No data showing
- Wait 2-3 seconds after triggering a scan
- Check browser console for errors (F12)
- Verify backend is running: `curl http://localhost:8000/`

### Can't connect to GCP
- Don't worry! Use `USE_MOCK_GCP=true` (default)
- Mock mode works perfectly for the assessment

## Development

### Backend
- FastAPI auto-reload enabled in debug mode
- Database: `shadow_ai.db` (SQLite file)
- Logs appear in backend terminal

### Frontend
- Vite HMR (Hot Module Replacement) enabled
- Changes auto-refresh in browser
- API calls proxied through Vite dev server

## Next Steps

1. Explore the UI and familiarize yourself with the features
2. Read `ARCHITECTURE.md` for design decisions
3. Check out the code in `backend/` and `frontend/src/`
4. When ready, set up real GCP following `GCP_SETUP_FREE.md`

## Need Help?

- **Architecture questions:** See `ARCHITECTURE.md`
- **GCP setup:** See `GCP_SETUP_FREE.md`
- **API documentation:** Visit http://localhost:8000/docs
- **Check progress:** See `CHECKLIST.md`

That's it! You now have a fully functional Shadow AI Discovery Engine running locally. 🎉
