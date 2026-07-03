# Taking Screenshots for Documentation

## Required Screenshots

Take the following screenshots and save them to the `screenshots/` folder:

### 1. Dashboard View
**Filename:** `01_dashboard.png`
**URL:** http://localhost:5173/
**What to show:**
- Overall statistics (Total Assets, AI Agents, Avg Confidence, High Risk)
- Assets by Type breakdown
- Quick action buttons

**How to capture:**
- Refresh the page if needed to show latest data
- Make sure the scan has completed
- Capture the full browser window

---

### 2. Assets View
**Filename:** `02_assets_view.png`
**URL:** http://localhost:5173/assets
**What to show:**
- Filter buttons at top
- Grid of asset cards
- Different resource types visible
- Resource details (runtime, service account, labels)

**Tips:**
- Make sure at least 6 cards are visible
- Show different resource types (Cloud Run, Functions, GKE)

---

### 3. Agents Table
**Filename:** `03_agents_table.png`
**URL:** http://localhost:5173/agents
**What to show:**
- Table with multiple agents
- Confidence scores (with progress bars)
- Risk badges (Low/Medium/High)
- Indicators preview
- Different resource types

**Tips:**
- Scroll to show at least 5-6 agents
- Make sure confidence bars are visible

---

### 4. Agent Details - High Confidence
**Filename:** `04_agent_details_high_confidence.png`
**URL:** http://localhost:5173/agents/agent-cloud-run-001
**What to show:**
- Header with name and confidence (100%)
- Confidence Score Breakdown section
- Multiple reasoning items with different severities
- Detected indicators

**Tips:**
- This is the most important screenshot
- Shows how confidence scoring works
- Capture enough to see 3-4 reason cards

---

### 5. Agent Details - Risk Assessment
**Filename:** `05_agent_details_risk.png`
**URL:** http://localhost:5173/agents/agent-gke-001
**What to show:**
- Risk Assessment section
- Risk factors with severity
- High risk score (90)
- Multiple risk indicators

**Tips:**
- Scroll to Risk Assessment section
- Show the critical risk factors

---

### 6. Agent Details - Environment & Metadata
**Filename:** `06_agent_details_metadata.png`
**URL:** http://localhost:5173/agents/agent-cloud-run-001
**What to show:**
- Environment Variables (with masked values)
- Resource Metadata section
- Labels
- Dependencies list

**Tips:**
- Scroll down to show these sections
- Show how sensitive data is masked

---

### 7. API Documentation
**Filename:** `07_api_docs.png`
**URL:** http://localhost:8000/docs
**What to show:**
- FastAPI Swagger UI
- List of endpoints
- Expanded view of one endpoint (e.g., GET /agents)

**Tips:**
- This shows the auto-generated API documentation
- Click on one endpoint to expand it

---

### 8. API Response Example
**Filename:** `08_api_response.png`
**Tool:** Terminal or Postman
**Command:** `curl http://localhost:8000/agents | jq`
**What to show:**
- JSON response from API
- Pretty-printed with syntax highlighting
- Shows real data structure

**Tips:**
- Use `jq` for pretty printing
- Or use Postman for a nice UI
- Capture about 20-30 lines of JSON

---

## Quick Screenshot Workflow

### Option 1: macOS
```bash
# Full window
Cmd + Shift + 4, then press Space, click window

# Selection
Cmd + Shift + 4, drag to select area
```

### Option 2: Windows
```bash
# Full window
Alt + PrtScn

# Selection
Windows + Shift + S
```

### Option 3: Chrome DevTools
1. Open DevTools (F12)
2. Cmd/Ctrl + Shift + P
3. Type "screenshot"
4. Choose "Capture full size screenshot" or "Capture screenshot"

---

## After Taking Screenshots

1. Name files as specified above
2. Save to `screenshots/` folder
3. Compress if files are > 2MB each
4. Add a README in screenshots folder listing what each shows

---

## Screenshots README Template

Create `screenshots/README.md`:

```markdown
# Screenshots

## Dashboard
![Dashboard](01_dashboard.png)
Overview with statistics and quick actions

## Assets View
![Assets View](02_assets_view.png)
All discovered cloud resources with filtering

## Agents Table
![Agents Table](03_agents_table.png)
Detected AI agents with confidence and risk scores

## Agent Details
![Agent Details](04_agent_details_high_confidence.png)
Detailed confidence breakdown for high-confidence agent

![Risk Assessment](05_agent_details_risk.png)
Risk assessment for high-risk agent

![Metadata](06_agent_details_metadata.png)
Environment variables and resource metadata

## API Documentation
![API Docs](07_api_docs.png)
Auto-generated FastAPI documentation

## API Response
![API Response](08_api_response.png)
Example JSON response from agents endpoint
```

---

That's it! These screenshots will demonstrate all key features of your Shadow AI Discovery Engine.
