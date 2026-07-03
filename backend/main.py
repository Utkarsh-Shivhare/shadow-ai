"""
Shadow AI Discovery Engine - FastAPI Backend

Main API endpoints for discovering and analyzing Shadow AI workloads
"""

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict
import uuid
from datetime import datetime
import os

from backend.database import get_db, Asset, Agent, Scan
from backend.scanner.gcp_scanner import GCPScanner
from backend.detector.ai_detector import detect_ai_agent

# Initialize FastAPI app
app = FastAPI(
    title="Shadow AI Discovery Engine",
    description="Discover and analyze AI workloads in Google Cloud Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Helper Functions ---

def save_asset_to_db(db: Session, resource: Dict) -> Asset:
    """Save or update asset in database"""
    asset = db.query(Asset).filter(Asset.id == resource['id']).first()
    
    if asset:
        # Update existing
        asset.name = resource['name']
        asset.resource_type = resource['resource_type']
        asset.region = resource.get('region')
        asset.runtime = resource.get('runtime')
        asset.service_account = resource.get('service_account')
        asset.is_public = resource.get('is_public', False)
        asset.logging_enabled = resource.get('logging_enabled', True)
        asset.environment = resource.get('environment', {})
        asset.labels = resource.get('labels', {})
        asset.dependencies = resource.get('dependencies', [])
        asset.last_seen = datetime.utcnow()
    else:
        # Create new
        asset = Asset(
            id=resource['id'],
            name=resource['name'],
            resource_type=resource['resource_type'],
            region=resource.get('region'),
            runtime=resource.get('runtime'),
            service_account=resource.get('service_account'),
            is_public=resource.get('is_public', False),
            logging_enabled=resource.get('logging_enabled', True),
            environment=resource.get('environment', {}),
            labels=resource.get('labels', {}),
            dependencies=resource.get('dependencies', []),
            discovered_at=datetime.utcnow(),
            last_seen=datetime.utcnow()
        )
        db.add(asset)
    
    db.commit()
    db.refresh(asset)
    return asset


def save_agent_to_db(db: Session, asset_id: str, detection_result: Dict) -> Agent:
    """Save or update agent detection in database"""
    agent_id = f"agent-{asset_id}"
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    
    if agent:
        # Update existing
        agent.confidence_score = detection_result['confidence_score']
        agent.risk_score = detection_result.get('risk_score', 0)
        agent.indicators = detection_result['indicators']
        agent.reasons = detection_result['reasons']
        agent.risk_factors = detection_result.get('risk_factors', [])
        agent.updated_at = datetime.utcnow()
    else:
        # Create new
        agent = Agent(
            id=agent_id,
            asset_id=asset_id,
            confidence_score=detection_result['confidence_score'],
            risk_score=detection_result.get('risk_score', 0),
            indicators=detection_result['indicators'],
            reasons=detection_result['reasons'],
            risk_factors=detection_result.get('risk_factors', []),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(agent)
    
    db.commit()
    db.refresh(agent)
    return agent


def perform_scan(scan_id: str, project_id: str, db: Session):
    """Background task to perform the actual scan"""
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    
    try:
        # Initialize scanner
        scanner = GCPScanner(project_id)
        
        # Scan all resources
        resources = scanner.scan_all_resources()
        
        assets_count = 0
        agents_count = 0
        
        # Process each resource
        for resource in resources:
            # Save asset
            asset = save_asset_to_db(db, resource)
            assets_count += 1
            
            # Detect AI
            detection = detect_ai_agent(resource)
            
            # If AI detected, save agent
            if detection['is_ai_agent']:
                save_agent_to_db(db, asset.id, detection)
                agents_count += 1
        
        # Update scan status
        scan.status = 'completed'
        scan.assets_found = assets_count
        scan.agents_found = agents_count
        scan.completed_at = datetime.utcnow()
        
    except Exception as e:
        # Handle errors
        scan.status = 'failed'
        scan.errors = [{'error': str(e)}]
        scan.completed_at = datetime.utcnow()
    
    db.commit()


# --- API Endpoints ---

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "service": "Shadow AI Discovery Engine",
        "status": "running",
        "version": "1.0.0",
        "mode": "mock" if os.getenv('USE_MOCK_GCP', 'true').lower() == 'true' else "real"
    }


@app.get("/assets", response_model=Dict)
def list_assets(
    resource_type: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all discovered cloud assets
    
    - **resource_type**: Filter by type (cloud_run, cloud_function, gke, vertex_ai)
    - **skip**: Pagination offset
    - **limit**: Number of results to return
    """
    query = db.query(Asset)
    
    # Filter by resource type if specified
    if resource_type:
        query = query.filter(Asset.resource_type == resource_type)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    assets = query.offset(skip).limit(limit).all()
    
    # Group by resource type
    by_type = {}
    for asset in db.query(Asset).all():
        rt = asset.resource_type
        by_type[rt] = by_type.get(rt, 0) + 1
    
    return {
        "total": total,
        "by_type": by_type,
        "assets": [asset.to_dict() for asset in assets]
    }


@app.get("/assets/{asset_id}", response_model=Dict)
def get_asset(asset_id: str, db: Session = Depends(get_db)):
    """Get details for a specific asset"""
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    return asset.to_dict()


@app.get("/agents", response_model=Dict)
def list_agents(
    min_confidence: int = 0,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all detected AI agents
    
    - **min_confidence**: Minimum confidence score (0-100)
    - **skip**: Pagination offset
    - **limit**: Number of results to return
    """
    query = db.query(Agent).filter(Agent.confidence_score >= min_confidence)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    agents = query.offset(skip).limit(limit).all()
    
    # Build response with asset info
    results = []
    for agent in agents:
        agent_dict = agent.to_dict(include_asset=False)
        if agent.asset:
            agent_dict['name'] = agent.asset.name
            agent_dict['resource_type'] = agent.asset.resource_type
            agent_dict['region'] = agent.asset.region
            agent_dict['runtime'] = agent.asset.runtime
        results.append(agent_dict)
    
    return {
        "total": total,
        "agents": results
    }


@app.get("/agents/{agent_id}", response_model=Dict)
def get_agent(agent_id: str, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific AI agent
    
    Returns full detection details including:
    - Confidence score breakdown
    - All detected indicators
    - Risk assessment
    - Asset metadata
    """
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    result = agent.to_dict(include_asset=True)
    
    return result


@app.post("/scan", response_model=Dict)
def trigger_scan(
    background_tasks: BackgroundTasks,
    project_id: str = None,
    db: Session = Depends(get_db)
):
    """
    Trigger a new discovery scan
    
    - **project_id**: GCP project ID (optional, uses default from config)
    
    Scan runs in background and returns immediately with scan ID.
    Use GET /scans/{scan_id} to check status.
    """
    # Use default project ID if not provided
    if not project_id:
        project_id = os.getenv('GCP_PROJECT_ID', 'mock-project')
    
    # Create scan record
    scan_id = f"scan-{uuid.uuid4().hex[:8]}"
    scan = Scan(
        id=scan_id,
        project_id=project_id,
        status='running',
        started_at=datetime.utcnow()
    )
    db.add(scan)
    db.commit()
    
    # Run scan in background
    background_tasks.add_task(perform_scan, scan_id, project_id, db)
    
    return {
        "scan_id": scan_id,
        "project_id": project_id,
        "status": "started",
        "message": "Scan started in background. Use GET /scans/{scan_id} to check status."
    }


@app.get("/scans/{scan_id}", response_model=Dict)
def get_scan_status(scan_id: str, db: Session = Depends(get_db)):
    """Get status of a scan"""
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    return scan.to_dict()


@app.get("/scans", response_model=Dict)
def list_scans(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """List recent scans"""
    total = db.query(Scan).count()
    scans = db.query(Scan).order_by(Scan.started_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "scans": [scan.to_dict() for scan in scans]
    }


@app.get("/stats", response_model=Dict)
def get_statistics(db: Session = Depends(get_db)):
    """Get overall statistics"""
    total_assets = db.query(Asset).count()
    total_agents = db.query(Agent).count()
    
    # Count by resource type
    assets_by_type = {}
    for asset in db.query(Asset).all():
        rt = asset.resource_type
        assets_by_type[rt] = assets_by_type.get(rt, 0) + 1
    
    # Average confidence
    agents = db.query(Agent).all()
    avg_confidence = sum(a.confidence_score for a in agents) / len(agents) if agents else 0
    avg_risk = sum(a.risk_score for a in agents) / len(agents) if agents else 0
    
    # High risk agents (risk > 50)
    high_risk = db.query(Agent).filter(Agent.risk_score > 50).count()
    
    return {
        "total_assets": total_assets,
        "total_agents": total_agents,
        "detection_rate": f"{(total_agents / total_assets * 100):.1f}%" if total_assets > 0 else "0%",
        "assets_by_type": assets_by_type,
        "average_confidence": round(avg_confidence, 1),
        "average_risk": round(avg_risk, 1),
        "high_risk_agents": high_risk
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('API_PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
