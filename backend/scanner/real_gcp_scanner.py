"""
Real GCP Client - For when you have GCP credentials

This file will be used when USE_MOCK_GCP=false
Currently contains placeholder - implement when you have GCP account
"""

from typing import List, Dict
from google.cloud import run_v2, functions_v2, container_v1, aiplatform
from google.oauth2 import service_account
import os


class RealGCPClient:
    """Real GCP API client using service account credentials"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        
        # Load credentials
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if not credentials_path:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS not set")
        
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        
        # Initialize clients
        self.run_client = run_v2.ServicesClient(credentials=self.credentials)
        self.functions_client = functions_v2.FunctionServiceClient(credentials=self.credentials)
        self.container_client = container_v1.ClusterManagerClient(credentials=self.credentials)
        
        print(f"☁️  RealGCPClient initialized for project: {project_id}")
    
    def scan_all_resources(self) -> List[Dict]:
        """Scan all GCP resources"""
        resources = []
        resources.extend(self.list_cloud_run_services())
        resources.extend(self.list_cloud_functions())
        resources.extend(self.list_gke_workloads())
        resources.extend(self.list_vertex_ai_endpoints())
        return resources
    
    def list_cloud_run_services(self) -> List[Dict]:
        """List Cloud Run services using real GCP API"""
        services = []
        
        try:
            parent = f"projects/{self.project_id}/locations/-"
            request = run_v2.ListServicesRequest(parent=parent)
            
            for service in self.run_client.list_services(request=request):
                service_name = service.name.split('/')[-1]
                location = service.name.split('/')[3]
                
                # Extract environment variables
                env_vars = {}
                if service.template and service.template.containers:
                    for container in service.template.containers:
                        if container.env:
                            for env in container.env:
                                env_vars[env.name] = env.value if env.value else '***'
                
                # Extract labels
                labels = dict(service.labels) if service.labels else {}
                
                # Get service account
                service_account = ''
                if service.template and service.template.service_account:
                    service_account = service.template.service_account
                
                services.append({
                    'id': f"cloud-run-{service_name}",
                    'name': service_name,
                    'resource_type': 'cloud_run',
                    'region': location,
                    'runtime': self._extract_runtime(service),
                    'service_account': service_account,
                    'is_public': self._check_if_public(service),
                    'logging_enabled': True,  # Cloud Run has logging by default
                    'environment': env_vars,
                    'labels': labels,
                    'dependencies': [],
                    'discovered_at': service.create_time.isoformat() if service.create_time else None,
                })
        except Exception as e:
            print(f"⚠️  Error scanning Cloud Run: {e}")
        
        return services
    
    def list_cloud_functions(self) -> List[Dict]:
        """List Cloud Functions using real GCP API"""
        functions = []
        
        try:
            parent = f"projects/{self.project_id}/locations/-"
            request = functions_v2.ListFunctionsRequest(parent=parent)
            
            for function in self.functions_client.list_functions(request=request):
                function_name = function.name.split('/')[-1]
                location = function.name.split('/')[3]
                
                # Extract environment variables
                env_vars = {}
                if function.build_config and function.build_config.environment_variables:
                    env_vars = dict(function.build_config.environment_variables)
                if function.service_config and function.service_config.environment_variables:
                    env_vars.update(dict(function.service_config.environment_variables))
                
                # Extract labels
                labels = dict(function.labels) if function.labels else {}
                
                # Get service account
                service_account = ''
                if function.service_config and function.service_config.service_account_email:
                    service_account = function.service_config.service_account_email
                
                functions.append({
                    'id': f"cloud-function-{function_name}",
                    'name': function_name,
                    'resource_type': 'cloud_function',
                    'region': location,
                    'runtime': function.build_config.runtime if function.build_config else 'unknown',
                    'service_account': service_account,
                    'is_public': False,  # Would need to check IAM bindings
                    'logging_enabled': True,
                    'environment': env_vars,
                    'labels': labels,
                    'dependencies': [],
                    'discovered_at': function.create_time.isoformat() if function.create_time else None,
                })
        except Exception as e:
            print(f"⚠️  Error scanning Cloud Functions: {e}")
        
        return functions
    
    def list_gke_workloads(self) -> List[Dict]:
        """List GKE clusters using real GCP API"""
        workloads = []
        
        try:
            parent = f"projects/{self.project_id}/locations/-"
            
            for cluster in self.container_client.list_clusters(parent=parent).clusters:
                cluster_name = cluster.name
                location = cluster.location
                
                # Basic cluster info as a workload
                workloads.append({
                    'id': f"gke-{cluster_name}",
                    'name': cluster_name,
                    'resource_type': 'gke',
                    'cluster': cluster_name,
                    'namespace': 'default',
                    'region': location,
                    'runtime': f"k8s-{cluster.current_master_version}" if cluster.current_master_version else 'unknown',
                    'service_account': cluster.node_config.service_account if cluster.node_config else '',
                    'is_public': cluster.private_cluster_config is None,
                    'logging_enabled': cluster.logging_service != 'none',
                    'environment': {},
                    'labels': dict(cluster.resource_labels) if cluster.resource_labels else {},
                    'dependencies': [],
                    'discovered_at': cluster.create_time if cluster.create_time else None,
                })
        except Exception as e:
            print(f"⚠️  Error scanning GKE: {e}")
        
        return workloads
    
    def list_vertex_ai_endpoints(self) -> List[Dict]:
        """List Vertex AI endpoints using real GCP API"""
        endpoints = []
        
        try:
            aiplatform.init(project=self.project_id, credentials=self.credentials)
            
            for endpoint in aiplatform.Endpoint.list():
                endpoints.append({
                    'id': f"vertex-{endpoint.name.split('/')[-1]}",
                    'name': endpoint.display_name or endpoint.name.split('/')[-1],
                    'resource_type': 'vertex_ai',
                    'region': endpoint.name.split('/')[3] if len(endpoint.name.split('/')) > 3 else 'us-central1',
                    'runtime': 'vertex-ai',
                    'service_account': '',
                    'is_public': False,
                    'logging_enabled': True,
                    'environment': {
                        'ENDPOINT_ID': endpoint.name,
                    },
                    'labels': dict(endpoint.labels) if endpoint.labels else {},
                    'dependencies': [],
                    'discovered_at': endpoint.create_time.isoformat() if hasattr(endpoint, 'create_time') and endpoint.create_time else None,
                })
        except Exception as e:
            print(f"⚠️  Error scanning Vertex AI: {e}")
        
        return endpoints
    
    def get_project_info(self) -> Dict:
        """Get real GCP project information"""
        return {
            'project_id': self.project_id,
            'project_name': self.project_id,
            'state': 'ACTIVE'
        }
    
    def _extract_runtime(self, service) -> str:
        """Extract runtime from Cloud Run service"""
        if service.template and service.template.containers:
            for container in service.template.containers:
                if container.image:
                    # Try to extract runtime from image
                    image = container.image.lower()
                    if 'python' in image:
                        return 'python'
                    elif 'node' in image:
                        return 'nodejs'
                    elif 'go' in image:
                        return 'go'
                    elif 'java' in image:
                        return 'java'
        return 'unknown'
    
    def _check_if_public(self, service) -> bool:
        """Check if Cloud Run service is publicly accessible"""
        # A service is public if it has allUsers invoker permission
        # This is a simplified check
        if service.template and service.template.service_account:
            return True  # Simplified - would need to check IAM policy
        return False
