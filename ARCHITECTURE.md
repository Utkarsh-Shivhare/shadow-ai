# Shadow AI Discovery Engine - Architecture

## Overview
A discovery platform to identify AI-enabled workloads in Google Cloud Platform without spending money on the assessment.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (React)                     │
│  - Assets View  - Agents View  - Agent Details  - Scan      │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST
┌────────────────────────▼────────────────────────────────────┐
│                    Backend API (FastAPI)                     │
│  GET /assets  GET /agents  GET /agents/{id}  POST /scan     │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ GCP Scanner  │  │  AI Detector │  │   Database   │
│              │  │              │  │  (SQLite)    │
│ - Cloud Run  │  │ - Heuristics │  │              │
│ - Functions  │  │ - Confidence │  │ - Assets     │
│ - GKE        │  │ - Scoring    │  │ - Agents     │
│ - Vertex AI  │  │              │  │ - Scans      │
└──────┬───────┘  └──────────────┘  └──────────────┘
       │
       ▼
┌──────────────────────┐
│   GCP APIs (Free)    │
│ - Resource Manager   │
│ - Cloud Run API      │
│ - Cloud Functions    │
│ - Container API      │
└──────────────────────┘
```

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
  - Fast, modern, async support
  - Auto-generated API docs
  - Easy to build REST APIs

- **GCP SDK**: `google-cloud` Python libraries
  - `google-cloud-resource-manager`
  - `google-cloud-run`
  - `google-cloud-functions`
  - `google-cloud-container`
  - `google-cloud-aiplatform`

- **Database**: SQLite
  - No setup required
  - File-based (no server)
  - Free
  - Good for demo/assessment

- **ORM**: SQLAlchemy
  - Python standard
  - Easy migrations
  - Works with SQLite

### Frontend
- **Framework**: React + Vite
  - Fast development
  - Component-based
  - Modern tooling

- **UI Library**: TailwindCSS
  - Quick styling
  - No custom CSS needed
  - Professional look

- **HTTP Client**: Axios
  - Easy API calls
  - Promise-based

### Free GCP Strategy
**Option 1: GCP Free Tier** (Recommended)
- New GCP accounts get $300 credit for 90 days
- Many services have "always free" tier
- Use existing test projects

**Option 2: Mock Mode** (Fallback)
- Create mock GCP responses
- Simulate resources locally
- No real GCP project needed

## Database Schema

### Table: assets
```sql
CREATE TABLE assets (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    resource_type TEXT NOT NULL,  -- cloud_run, cloud_function, gke, vertex_ai
    region TEXT,
    runtime TEXT,
    service_account TEXT,
    labels JSON,
    environment_vars JSON,
    discovered_at TIMESTAMP,
    last_seen TIMESTAMP
);
```

### Table: agents
```sql
CREATE TABLE agents (
    id TEXT PRIMARY KEY,
    asset_id TEXT REFERENCES assets(id),
    confidence_score INTEGER,  -- 0-100
    indicators JSON,  -- list of detected indicators
    reasons JSON,     -- detailed scoring breakdown
    risk_score INTEGER,  -- bonus feature
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Table: scans
```sql
CREATE TABLE scans (
    id TEXT PRIMARY KEY,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    status TEXT,  -- running, completed, failed
    assets_found INTEGER,
    agents_found INTEGER,
    errors JSON
);
```

## Core Components

### 1. GCP Scanner (`backend/scanner/gcp_scanner.py`)
**Responsibility**: Discover cloud resources

**Methods**:
- `scan_cloud_run()` - List Cloud Run services
- `scan_cloud_functions()` - List Cloud Functions
- `scan_gke()` - List GKE clusters and workloads
- `scan_vertex_ai()` - List Vertex AI endpoints/models
- `get_resource_metadata()` - Extract env vars, labels, SA

**Output**: List of discovered assets with metadata

### 2. AI Detector (`backend/detector/ai_detector.py`)
**Responsibility**: Identify AI workloads

**Heuristics**:
- Environment variable scanning
  - `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`
  - `GEMINI_API_KEY`, `COHERE_API_KEY`
- Label detection
  - `ai-enabled`, `langchain`, `llm`
- Runtime analysis
  - Python with AI libraries
  - Container image inspection
- Vertex AI integration
  - Service account permissions
  - API call patterns

**Confidence Scoring Logic**:
```python
base_score = 0

# Environment variables (+30 each)
if has_llm_api_keys: base_score += 30

# AI Frameworks (+25 each)
if has_langchain: base_score += 25
if has_llamaindex: base_score += 25

# Vertex AI (+20)
if uses_vertex_ai: base_score += 20

# Labels (+15)
if has_ai_labels: base_score += 15

# Container analysis (+20)
if dockerfile_has_ai_libs: base_score += 20

confidence = min(base_score, 100)
```

### 3. REST API (`backend/main.py`)

**Endpoints**:

```
GET /assets
Response: {
  "total": 15,
  "assets": [
    {
      "id": "cloud-run-123",
      "name": "my-service",
      "type": "cloud_run",
      "region": "us-central1",
      "runtime": "python311"
    }
  ]
}

GET /agents
Response: {
  "total": 3,
  "agents": [
    {
      "id": "agent-456",
      "name": "my-ai-service",
      "confidence": 94,
      "runtime": "python311",
      "risk": "high"
    }
  ]
}

GET /agents/{id}
Response: {
  "id": "agent-456",
  "name": "my-ai-service",
  "confidence": 94,
  "indicators": ["langchain", "openai_key", "vertex_ai"],
  "reasons": [
    "LangGraph detected (+25)",
    "OPENAI_API_KEY configured (+30)",
    "Vertex AI client library present (+20)"
  ],
  "environment": { "OPENAI_API_KEY": "***", "MODEL": "gpt-4" },
  "service_account": "ai-service@project.iam",
  "discovered_at": "2026-07-02T10:30:00Z"
}

POST /scan
Request: { "project_id": "my-gcp-project" }
Response: {
  "scan_id": "scan-789",
  "status": "started",
  "started_at": "2026-07-02T10:35:00Z"
}
```

### 4. Frontend Components

**Pages**:
- `AssetsView.jsx` - List all assets with filters
- `AgentsView.jsx` - Table of detected agents
- `AgentDetails.jsx` - Detailed view with confidence breakdown
- `ScanTrigger.jsx` - Button to start new scan

## Key Design Decisions

### 1. SQLite over PostgreSQL
**Why**: No setup, no cost, sufficient for demo
**Trade-off**: Limited concurrent writes (not an issue for assessment)
**Production**: Would use PostgreSQL or Cloud SQL

### 2. Synchronous Scanning
**Why**: Simple implementation, easier to debug
**Trade-off**: Slower for large projects
**Production**: Would use async workers (Celery/Cloud Tasks)

### 3. Heuristic-Based Detection
**Why**: No ML training needed, explainable results
**Trade-off**: May miss novel patterns
**Production**: Could add ML model for better detection

### 4. In-Memory Caching
**Why**: Fast repeated access, no external dependencies
**Trade-off**: Lost on restart
**Production**: Would use Redis/Memorystore

## Scaling to Thousands of Projects

### Current Limitations
- Sequential scanning (one project at a time)
- Single server instance
- SQLite write bottleneck
- No caching layer

### Production Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                        │
└────────────────────────┬────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  API Server  │  │  API Server  │  │  API Server  │
│   (FastAPI)  │  │   (FastAPI)  │  │   (FastAPI)  │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └────────────────┬─────────────────┘
                        │
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Scan Worker  │  │ Scan Worker  │  │ Scan Worker  │
│  (Celery)    │  │  (Celery)    │  │  (Celery)    │
└──────────────┘  └──────────────┘  └──────────────┘
       │                 │                 │
       └────────────────┬─────────────────┘
                        │
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  PostgreSQL  │  │  Redis Cache │  │  Cloud Pub/Sub│
│  (Cloud SQL) │  │ (Memorystore)│  │  (Queue)      │
└──────────────┘  └──────────────┘  └──────────────┘
```

### Scaling Strategies

**1. Parallel Project Scanning**
- Use Cloud Pub/Sub or RabbitMQ for job queue
- Worker pool processes multiple projects simultaneously
- Each project gets its own scan task

**2. Resource-Level Parallelization**
- Scan Cloud Run, Functions, GKE, Vertex AI in parallel
- Use async/await for concurrent API calls
- Batch API requests where possible

**3. Caching**
- Cache GCP API responses (5-15 min TTL)
- Cache agent detection results
- Incremental scanning (only scan changed resources)

**4. Database Optimization**
- PostgreSQL with connection pooling
- Partitioning by project_id
- Indexes on frequently queried fields
- Read replicas for dashboard queries

**5. Rate Limiting**
- Respect GCP API quotas (1000 req/min typical)
- Exponential backoff on errors
- Distributed rate limiting with Redis

**6. Monitoring**
- Track scan duration per project
- Alert on failures
- Dashboard for scan health

### Estimated Capacity

**Current (Single Server)**:
- ~10 projects/hour
- ~100 resources/minute

**Production (Scaled)**:
- ~1000 projects/hour (10 workers)
- ~10,000 resources/minute (parallel scanning)
- Support for 10,000+ projects daily

## Security Considerations

### GCP Permissions (Least Privilege)
The service account needs READ-ONLY access:
```
roles/viewer                    # Basic read access
roles/cloudfunctions.viewer
roles/run.viewer
roles/container.viewer
roles/aiplatform.viewer
```

### Sensitive Data Handling
- Never store full API keys (mask after first 4 chars)
- Redact secret environment variables
- Encrypt database at rest (production)
- Audit log all scans

### API Security
- Add API authentication (JWT tokens)
- Rate limiting per client
- Input validation
- CORS configuration

## Development Phases

### Phase 1: Core Backend (4 hours)
- [ ] FastAPI setup
- [ ] GCP authentication
- [ ] Basic scanner for Cloud Run
- [ ] SQLite database setup
- [ ] Simple AI detection

### Phase 2: Full Scanning (2 hours)
- [ ] Cloud Functions scanner
- [ ] GKE scanner
- [ ] Vertex AI scanner
- [ ] Confidence scoring logic

### Phase 3: API & Storage (2 hours)
- [ ] Complete REST endpoints
- [ ] Database models
- [ ] CRUD operations

### Phase 4: Frontend (3 hours)
- [ ] React setup
- [ ] Assets view
- [ ] Agents view
- [ ] Agent details page

### Phase 5: Polish (1 hour)
- [ ] Documentation
- [ ] README
- [ ] Sample data
- [ ] Screenshots

## Testing Strategy

### Unit Tests
- Test confidence scoring logic
- Test API endpoint responses
- Test database operations

### Integration Tests
- Test GCP API interactions (mocked)
- Test end-to-end scan flow

### Manual Testing
- Run against real/mock GCP project
- Verify UI displays correctly
- Test API with Postman/curl

## Dependencies

### Backend
```
fastapi==0.104.0
uvicorn==0.24.0
sqlalchemy==2.0.23
google-cloud-resource-manager==1.11.0
google-cloud-run==0.9.0
google-cloud-functions==1.14.0
google-cloud-container==2.36.0
google-cloud-aiplatform==1.38.0
pydantic==2.5.0
python-dotenv==1.0.0
```

### Frontend
```
react==18.2.0
react-router-dom==6.20.0
axios==1.6.2
tailwindcss==3.3.5
```

## File Structure

```
shadow_ai/
├── backend/
│   ├── main.py                 # FastAPI app
│   ├── database.py             # SQLAlchemy models
│   ├── scanner/
│   │   ├── gcp_scanner.py      # GCP resource discovery
│   │   └── auth.py             # GCP authentication
│   ├── detector/
│   │   ├── ai_detector.py      # AI detection logic
│   │   └── confidence.py       # Scoring algorithm
│   ├── models/
│   │   ├── asset.py
│   │   ├── agent.py
│   │   └── scan.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AssetsView.jsx
│   │   │   ├── AgentsView.jsx
│   │   │   └── AgentDetails.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── ARCHITECTURE.md             # This file
├── README.md
└── .env.example
```

## Cost Analysis (Why This Won't Cost Money)

### GCP Free Tier (Always Free)
- Cloud Run: 2 million requests/month
- Cloud Functions: 2 million invocations/month
- GKE: First cluster free (zonal)
- API calls: Generally free for listing resources

### Our Usage
- API calls: ~100-500 per scan (well under limits)
- Compute: Running locally (no cloud hosting)
- Storage: SQLite (local, free)

### To Avoid Costs
- Don't deploy to Cloud Run (run locally)
- Use read-only API calls
- Don't create new resources
- Use existing test project or mock mode
