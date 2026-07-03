"""
GCP Scanner - Discovers cloud resources from GCP

Supports both REAL GCP (with service account) and MOCK mode (no GCP needed)
Toggle with USE_MOCK_GCP environment variable
"""

import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()


class GCPScanner:
    """Unified scanner that works with both mock and real GCP"""
    
    def __init__(self, project_id: str = None, use_mock: bool = None):
        self.project_id = project_id or os.getenv('GCP_PROJECT_ID', 'mock-project')
        self.use_mock = use_mock if use_mock is not None else os.getenv('USE_MOCK_GCP', 'true').lower() == 'true'
        
        if self.use_mock:
            print(f"🔧 Using MOCK mode for project: {self.project_id}")
            from backend.scanner.mock_gcp import MockGCPClient
            self.client = MockGCPClient(self.project_id)
        else:
            print(f"☁️  Using REAL GCP for project: {self.project_id}")
            try:
                from backend.scanner.real_gcp_scanner import RealGCPClient
                self.client = RealGCPClient(self.project_id)
            except ImportError:
                print("⚠️  Real GCP client not available, falling back to MOCK mode")
                from backend.scanner.mock_gcp import MockGCPClient
                self.client = MockGCPClient(self.project_id)
                self.use_mock = True
    
    def scan_all_resources(self) -> List[Dict]:
        """
        Scan all supported GCP resources
        
        Returns:
            List of resource dictionaries with metadata
        """
        print(f"🔍 Scanning GCP project: {self.project_id}")
        resources = self.client.scan_all_resources()
        print(f"✓ Found {len(resources)} resources")
        return resources
    
    def scan_cloud_run(self) -> List[Dict]:
        """Scan Cloud Run services"""
        return self.client.list_cloud_run_services()
    
    def scan_cloud_functions(self) -> List[Dict]:
        """Scan Cloud Functions"""
        return self.client.list_cloud_functions()
    
    def scan_gke(self) -> List[Dict]:
        """Scan GKE workloads"""
        return self.client.list_gke_workloads()
    
    def scan_vertex_ai(self) -> List[Dict]:
        """Scan Vertex AI endpoints"""
        return self.client.list_vertex_ai_endpoints()
    
    def get_project_info(self) -> Dict:
        """Get GCP project information"""
        return self.client.get_project_info()


# Convenience function for quick scanning
def scan_gcp_project(project_id: str = None) -> List[Dict]:
    """Quick scan function"""
    scanner = GCPScanner(project_id)
    return scanner.scan_all_resources()
