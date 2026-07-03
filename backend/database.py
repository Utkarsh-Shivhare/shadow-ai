"""
Database models for Shadow AI Discovery Engine

Using SQLAlchemy with SQLite for simplicity
"""

from sqlalchemy import create_engine, Column, String, Integer, JSON, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./shadow_ai.db')
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if 'sqlite' in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Asset(Base):
    """Cloud resource asset"""
    __tablename__ = "assets"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    resource_type = Column(String, index=True, nullable=False)  # cloud_run, cloud_function, gke, vertex_ai
    region = Column(String)
    runtime = Column(String)
    service_account = Column(String)
    is_public = Column(Boolean, default=False)
    logging_enabled = Column(Boolean, default=True)
    
    # JSON fields
    environment = Column(JSON)  # Environment variables
    labels = Column(JSON)  # Resource labels
    dependencies = Column(JSON)  # List of dependencies
    
    # Timestamps
    discovered_at = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    agent = relationship("Agent", back_populates="asset", uselist=False)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'resource_type': self.resource_type,
            'region': self.region,
            'runtime': self.runtime,
            'service_account': self.service_account,
            'is_public': self.is_public,
            'logging_enabled': self.logging_enabled,
            'environment': self.environment or {},
            'labels': self.labels or {},
            'dependencies': self.dependencies or [],
            'discovered_at': self.discovered_at.isoformat() if self.discovered_at else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
        }


class Agent(Base):
    """AI Agent detection record"""
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, index=True)
    asset_id = Column(String, ForeignKey('assets.id'), unique=True, nullable=False)
    
    # Detection results
    confidence_score = Column(Integer, nullable=False)  # 0-100
    risk_score = Column(Integer, default=0)  # 0-100
    
    # JSON fields
    indicators = Column(JSON)  # List of detected indicators
    reasons = Column(JSON)  # List of reason objects
    risk_factors = Column(JSON)  # List of risk factor objects
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    asset = relationship("Asset", back_populates="agent")
    
    def to_dict(self, include_asset=False):
        """Convert to dictionary"""
        result = {
            'id': self.id,
            'asset_id': self.asset_id,
            'confidence_score': self.confidence_score,
            'risk_score': self.risk_score,
            'indicators': self.indicators or [],
            'reasons': self.reasons or [],
            'risk_factors': self.risk_factors or [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        
        if include_asset and self.asset:
            result['asset'] = self.asset.to_dict()
        
        return result


class Scan(Base):
    """Scan execution record"""
    __tablename__ = "scans"
    
    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, nullable=False)
    
    # Status
    status = Column(String, default='running')  # running, completed, failed
    
    # Results
    assets_found = Column(Integer, default=0)
    agents_found = Column(Integer, default=0)
    
    # Errors (if any)
    errors = Column(JSON)
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'project_id': self.project_id,
            'status': self.status,
            'assets_found': self.assets_found,
            'agents_found': self.agents_found,
            'errors': self.errors or [],
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }


# Database initialization
def init_db():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized")


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create tables on import
init_db()
