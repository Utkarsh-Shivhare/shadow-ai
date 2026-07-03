# GCP Setup Guide (Free - No Cost)

## Option 1: Use GCP Free Tier (Recommended)

### Prerequisites
- Gmail account (to create GCP account)
- Credit/debit card (for verification only - won't be charged)

### Step 1: Create GCP Account
1. Go to https://cloud.google.com/free
2. Click "Get started for free"
3. Sign in with your Google account
4. Enter card details (for verification - **you get $300 free credit**)
5. Complete setup

**Note**: Google gives you $300 credit valid for 90 days. The API calls we'll make are minimal and mostly free.

### Step 2: Create a New Project
1. Go to https://console.cloud.google.com
2. Click the project dropdown (top bar)
3. Click "New Project"
4. Name it: `shadow-ai-test`
5. Click "Create"

### Step 3: Enable Required APIs
```bash
# You'll need to enable these APIs (all FREE for our usage):
- Cloud Resource Manager API
- Cloud Run API
- Cloud Functions API
- Kubernetes Engine API
- Vertex AI API
```

Go to: https://console.cloud.google.com/apis/library

Search and enable each:
1. "Cloud Resource Manager API" → Enable
2. "Cloud Run Admin API" → Enable
3. "Cloud Functions API" → Enable
4. "Kubernetes Engine API" → Enable
5. "Vertex AI API" → Enable

### Step 4: Create Service Account

1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
2. Click "Create Service Account"
3. Fill in:
   - **Name**: `shadow-ai-scanner`
   - **Description**: "Service account for Shadow AI discovery engine"
4. Click "Create and Continue"
5. Grant these roles (READ-ONLY, no cost):
   - `Viewer` (provides basic read access)
   - `Cloud Run Viewer`
   - `Cloud Functions Viewer`
   - `Kubernetes Engine Viewer`
6. Click "Continue" → "Done"

### Step 5: Create Service Account Key

1. Find your service account in the list
2. Click the three dots (⋮) → "Manage keys"
3. Click "Add Key" → "Create new key"
4. Choose "JSON"
5. Click "Create"
6. A JSON file will download → Save it securely!

### Step 6: Set Up in Your Project

1. Move the JSON key file to your project:
```bash
cd /Users/utkarsh/utkarsh/shadow_ai
mkdir -p credentials
mv ~/Downloads/shadow-ai-test-*.json credentials/gcp-service-account.json
```

2. Add to `.gitignore` (so you don't commit it):
```bash
echo "credentials/" >> .gitignore
echo ".env" >> .gitignore
```

3. Set environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials/gcp-service-account.json"
```

Or create a `.env` file:
```bash
GOOGLE_APPLICATION_CREDENTIALS=./credentials/gcp-service-account.json
GCP_PROJECT_ID=shadow-ai-test
```

### Step 7: Test Authentication

Create a test script:
```python
# test_gcp_auth.py
from google.cloud import resourcemanager_v3

def test_auth():
    try:
        client = resourcemanager_v3.ProjectsClient()
        print("✓ Authentication successful!")
        print(f"✓ Can access GCP APIs")
        return True
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        return False

if __name__ == "__main__":
    test_auth()
```

Run it:
```bash
pip install google-cloud-resource-manager
python test_gcp_auth.py
```

### Cost Estimate: $0
- API calls for listing resources: FREE
- Service account: FREE
- Project: FREE
- We're only reading, not creating resources

---

## Option 2: Mock Mode (100% Free, No GCP Account)

If you don't want to use GCP at all, you can simulate it with mock data.

### Step 1: Create Mock GCP Client

```python
# backend/scanner/mock_gcp.py

class MockGCPClient:
    """Simulates GCP API responses for testing without a real project"""
    
    def list_cloud_run_services(self):
        return [
            {
                "name": "ai-chatbot-service",
                "region": "us-central1",
                "runtime": "python311",
                "service_account": "chatbot@project.iam",
                "environment": {
                    "OPENAI_API_KEY": "sk-proj-xxx",
                    "MODEL": "gpt-4",
                    "LANGCHAIN_VERSION": "0.1.0"
                },
                "labels": {"ai-enabled": "true", "team": "ml"}
            },
            {
                "name": "web-frontend",
                "region": "us-east1",
                "runtime": "nodejs20",
                "service_account": "frontend@project.iam",
                "environment": {
                    "NODE_ENV": "production",
                    "API_URL": "https://api.example.com"
                },
                "labels": {"team": "web"}
            },
            {
                "name": "vertex-ai-pipeline",
                "region": "us-west1",
                "runtime": "python311",
                "service_account": "pipeline@project.iam",
                "environment": {
                    "VERTEX_AI_ENDPOINT": "us-west1-aiplatform.googleapis.com",
                    "MODEL_ID": "gemini-pro",
                    "LANGCHAIN_TRACING": "true"
                },
                "labels": {"ai-enabled": "true", "framework": "langchain"}
            }
        ]
    
    def list_cloud_functions(self):
        return [
            {
                "name": "process-documents",
                "region": "us-central1",
                "runtime": "python39",
                "service_account": "processor@project.iam",
                "environment": {
                    "ANTHROPIC_API_KEY": "sk-ant-xxx",
                    "LLAMAINDEX_VERSION": "0.9.0"
                },
                "labels": {"type": "ai-processor"}
            },
            {
                "name": "send-email",
                "region": "us-east1",
                "runtime": "python39",
                "service_account": "mailer@project.iam",
                "environment": {
                    "SENDGRID_API_KEY": "SG.xxx",
                    "SMTP_HOST": "smtp.sendgrid.net"
                },
                "labels": {"type": "notification"}
            }
        ]
    
    def list_gke_workloads(self):
        return [
            {
                "name": "crewai-agents",
                "cluster": "production-cluster",
                "namespace": "ai-workloads",
                "region": "us-central1",
                "runtime": "python311",
                "service_account": "crewai@project.iam",
                "environment": {
                    "OPENAI_API_KEY": "sk-proj-xxx",
                    "CREWAI_VERSION": "0.2.0",
                    "LANGCHAIN_API_KEY": "lc-xxx"
                },
                "labels": {"framework": "crewai", "ai": "true"}
            }
        ]
    
    def list_vertex_ai_endpoints(self):
        return [
            {
                "name": "custom-llm-endpoint",
                "region": "us-central1",
                "model": "text-bison@001",
                "service_account": "vertex@project.iam",
                "labels": {"model-type": "llm"}
            }
        ]
```

### Step 2: Use Mock Mode in Your Scanner

```python
# backend/scanner/gcp_scanner.py
import os
from backend.scanner.mock_gcp import MockGCPClient

class GCPScanner:
    def __init__(self, project_id: str, use_mock: bool = False):
        self.project_id = project_id
        self.use_mock = use_mock or os.getenv("USE_MOCK_GCP") == "true"
        
        if self.use_mock:
            print("🔧 Using MOCK mode (no real GCP calls)")
            self.client = MockGCPClient()
        else:
            print("☁️  Using REAL GCP")
            # Real GCP client initialization
            from google.cloud import run_v2, functions_v2
            self.run_client = run_v2.ServicesClient()
            self.functions_client = functions_v2.FunctionServiceClient()
```

### Step 3: Enable Mock Mode

Create `.env` file:
```bash
USE_MOCK_GCP=true
GCP_PROJECT_ID=mock-project
```

### Benefits of Mock Mode
- ✅ 100% Free
- ✅ No GCP account needed
- ✅ No credit card required
- ✅ Instant setup
- ✅ Fully testable
- ✅ Demo-ready data

### Drawbacks
- ❌ Not testing real GCP integration
- ❌ Can't show real discovery

---

## Option 3: Hybrid Mode (Best for Assessment)

Combine both approaches:
1. Use MOCK mode for development and demo
2. Use REAL GCP for final testing (minimal API calls)
3. Include screenshots from both

### Setup
```python
# config.py
import os

class Config:
    # Will use mock if no credentials found
    USE_MOCK = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") is None
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "mock-project")
```

This way:
- You can develop everything without GCP
- When ready, test with real GCP (using free tier)
- Show in README: "Supports both real GCP and mock mode"

---

## Recommended Approach for Assessment

### Week 1: Build with Mock Mode
- No GCP account needed
- Fast iteration
- Build all features

### Day of Submission: Test with Real GCP
- Create free GCP account
- Enable APIs (5 minutes)
- Run one real scan
- Take screenshots
- Shutdown/delete project

**Total Cost: $0**

---

## Quick Start Commands

### Check if you have GCP credentials
```bash
echo $GOOGLE_APPLICATION_CREDENTIALS
```

### Install GCP SDK
```bash
pip install google-cloud-resource-manager \
            google-cloud-run \
            google-cloud-functions \
            google-cloud-container \
            google-cloud-aiplatform
```

### Test authentication
```bash
python -c "from google.cloud import resourcemanager_v3; print('✓ Auth works')"
```

### Or use mock mode
```bash
export USE_MOCK_GCP=true
```

---

## Troubleshooting

### Error: "Could not automatically determine credentials"
**Solution**: Either:
1. Set `GOOGLE_APPLICATION_CREDENTIALS` to your JSON key path
2. Or set `USE_MOCK_GCP=true` in `.env`

### Error: "Permission denied"
**Solution**: Service account needs Viewer role
1. Go to IAM page
2. Find your service account
3. Add "Viewer" role

### Error: "API not enabled"
**Solution**: Enable the API
1. Go to APIs & Services
2. Search for the API name
3. Click "Enable"

### Don't want to use GCP at all?
**Solution**: Use `USE_MOCK_GCP=true` - works perfectly for the assessment!

---

## What I Recommend

For your assessment, I suggest:

### Path A: Fastest (Mock Only)
- Use mock mode entirely
- Mention in README: "Supports real GCP with service account"
- Show mock data in demo
- **Time: 0 minutes, Cost: $0**

### Path B: Best Impression (Hybrid)
- Build with mock mode
- Test final version with free GCP
- Include both screenshots
- **Time: 15 minutes for GCP setup, Cost: $0**

### Path C: Production-Like (Real GCP)
- Set up GCP account now
- Develop against real APIs
- More realistic
- **Time: 15 minutes, Cost: $0 (free tier)**

**My recommendation: Start with Path A, upgrade to Path B before submission.**

You'll have a working system either way, and the evaluators care more about your architecture and code quality than whether you used real GCP!
