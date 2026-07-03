# Development Checklist

Use this checklist to track your progress through the assessment.

## ✅ Understanding Phase (DONE!)

- [x] Read the assignment document
- [x] Understand what Shadow AI Discovery means
- [x] Review ARCHITECTURE.md
- [x] Review GCP_SETUP_FREE.md
- [x] Understand the evaluation criteria

## 🔧 Setup Phase (Next: 30 mins)

### Choose Your Path
- [ ] **Option A**: Mock mode (fastest, no GCP account)
  - [ ] Set `USE_MOCK_GCP=true` in `.env`
  - [ ] Skip GCP setup entirely
  
- [ ] **Option B**: Real GCP (more impressive)
  - [ ] Create GCP account
  - [ ] Create project
  - [ ] Enable APIs
  - [ ] Create service account
  - [ ] Download JSON key

### Project Setup
- [ ] Create `.env` file
- [ ] Add `.gitignore`
- [ ] Create virtual environment
- [ ] Note your approach in README

## 🏗️ Backend Development (4-5 hours)

### Phase 1: Foundation (1 hour)
- [ ] Set up FastAPI project structure
- [ ] Install dependencies (`requirements.txt`)
- [ ] Configure database (SQLAlchemy + SQLite)
- [ ] Create database models (Asset, Agent, Scan)
- [ ] Test: Basic API responds at `http://localhost:8000`

### Phase 2: GCP Scanner (2 hours)
- [ ] Create GCP authentication module
- [ ] Implement Cloud Run scanner
- [ ] Implement Cloud Functions scanner
- [ ] Implement GKE scanner (basic)
- [ ] Implement Vertex AI scanner (basic)
- [ ] Test: Can list resources (mock or real)

### Phase 3: AI Detection (1 hour)
- [ ] Create AI detector module
- [ ] Implement environment variable scanning
- [ ] Implement label detection
- [ ] Implement confidence scoring logic
- [ ] Add reasoning/explanation for scores
- [ ] Test: Correctly identifies AI workloads

### Phase 4: REST API (1 hour)
- [ ] `GET /assets` - List all resources
- [ ] `GET /agents` - List AI agents only
- [ ] `GET /agents/{id}` - Get agent details
- [ ] `POST /scan` - Trigger new scan
- [ ] Test: All endpoints work with Postman/curl
- [ ] Add CORS for frontend

## 🎨 Frontend Development (3 hours)

### Phase 1: Setup (30 mins)
- [ ] Create React + Vite project
- [ ] Install dependencies (axios, react-router, tailwind)
- [ ] Configure Tailwind CSS
- [ ] Set up routing
- [ ] Test: Basic page loads

### Phase 2: Core Components (1.5 hours)
- [ ] Create Assets View (list all resources)
- [ ] Create Agents View (list AI agents table)
- [ ] Create Agent Details View (detailed breakdown)
- [ ] Create Scan button/trigger
- [ ] Test: All views render correctly

### Phase 3: Polish (1 hour)
- [ ] Add basic styling with Tailwind
- [ ] Add loading states
- [ ] Add error handling
- [ ] Make it responsive (mobile-friendly)
- [ ] Test: Looks presentable

## 📸 Documentation & Screenshots (2 hours)

### Screenshots (30 mins)
- [ ] Assets view (showing multiple resource types)
- [ ] Agents view (table with confidence scores)
- [ ] Agent details (showing reasoning)
- [ ] API response examples (Postman/curl)

### Documentation (1.5 hours)
- [ ] Update README with:
  - [ ] Setup instructions
  - [ ] How to run (backend + frontend)
  - [ ] API documentation
  - [ ] Screenshots embedded
  - [ ] Technology choices
- [ ] Finalize ARCHITECTURE.md with:
  - [ ] Design decisions explained
  - [ ] Trade-offs discussed
  - [ ] Production considerations
  - [ ] Scaling strategy
- [ ] Create `.env.example`
- [ ] Add comments to complex code
- [ ] Create sample API responses (JSON files)

## 🧪 Testing & Polish (1 hour)

- [ ] Test complete end-to-end flow:
  - [ ] Start backend
  - [ ] Start frontend
  - [ ] Trigger scan
  - [ ] View assets
  - [ ] View agents
  - [ ] View agent details
- [ ] Fix any bugs found
- [ ] Verify all API endpoints work
- [ ] Check console for errors
- [ ] Verify database is populated correctly

## 📦 Submission Prep (30 mins)

- [ ] Create GitHub repository
- [ ] Push all code
- [ ] Verify `.gitignore` works (no credentials committed!)
- [ ] Add screenshots to `/screenshots` folder
- [ ] Test: Clone repo in fresh directory and run it
- [ ] Update README with GitHub repo structure
- [ ] Final review of ARCHITECTURE.md

## 🎁 Bonus Features (Optional - If Time Permits)

### Bonus 1: Cloud Logging (1-2 hours)
- [ ] Integrate Cloud Logging API
- [ ] Detect Vertex AI API calls in logs
- [ ] Add to confidence scoring

### Bonus 2: Risk Scoring (30 mins)
- [ ] Create risk calculation logic
- [ ] Factor in: public endpoints, permissions, external LLMs
- [ ] Display risk in UI

### Bonus 3: Relationship Visualization (1-2 hours)
- [ ] Use a graph library (D3.js, vis.js)
- [ ] Show resource relationships
- [ ] Service Account → Secrets → APIs

### Bonus 4: Container Image Analysis (2 hours)
- [ ] Parse Dockerfile or image layers
- [ ] Detect AI libraries from pip/npm dependencies
- [ ] Add to detection logic

### Bonus 5: Incremental Scanning (1 hour)
- [ ] Track last scan timestamp per resource
- [ ] Only scan changed resources
- [ ] Show "Updated" vs "New" in UI

## 📊 Time Tracking

| Phase | Estimated | Actual | Notes |
|-------|-----------|--------|-------|
| Setup | 30m | | |
| Backend | 4-5h | | |
| Frontend | 3h | | |
| Documentation | 2h | | |
| Testing | 1h | | |
| Submission | 30m | | |
| **Total** | **11-12h** | | |

## 🎯 Minimum Viable Submission

If running short on time, ensure you have at least:

**Must Have** (70% of grade):
- ✅ Backend API with 2+ resource types
- ✅ AI detection with confidence scores
- ✅ Working endpoints (GET /agents at minimum)
- ✅ Basic UI showing agents list
- ✅ ARCHITECTURE.md with design decisions
- ✅ README with setup instructions

**Should Have** (20% of grade):
- ✅ All 4 resource types (Cloud Run, Functions, GKE, Vertex)
- ✅ Complete REST API
- ✅ Full UI (Assets + Agents + Details views)
- ✅ Good code quality

**Nice to Have** (10% of grade):
- ✅ One bonus feature
- ✅ Beautiful UI
- ✅ Comprehensive tests

## 🚨 Common Pitfalls to Avoid

- [ ] ❌ Don't commit GCP credentials to Git
- [ ] ❌ Don't spend too much time on UI polish
- [ ] ❌ Don't try to implement ALL bonus features
- [ ] ❌ Don't skip documentation
- [ ] ❌ Don't forget to test end-to-end
- [ ] ❌ Don't ignore the architecture document
- [ ] ❌ Don't make up GCP API responses (use mock or real)

## 🎉 Definition of Done

Your submission is complete when:

1. ✅ Code is on GitHub
2. ✅ README has clear setup instructions
3. ✅ ARCHITECTURE.md explains your decisions
4. ✅ Backend API works (tested with Postman/curl)
5. ✅ Frontend displays data correctly
6. ✅ Screenshots are included
7. ✅ You can explain every design choice
8. ✅ A fresh clone works (you tested it)

## 💪 You've Got This!

**Current Status**: Setup & Understanding Complete ✅

**Next Action**: Choose Mock or Real GCP, then start building the backend!

Remember:
- Focus on architecture and decisions (60% of grade)
- AI tools are encouraged - use them!
- Don't aim for perfection - aim for completion
- 8-12 hours is plenty of time with this roadmap

---

**Ready to start coding? Begin with "Setup Phase" above!** 🚀
