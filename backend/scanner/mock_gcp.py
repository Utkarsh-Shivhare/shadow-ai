"""
Mock GCP Client - Simulates GCP API responses for testing

This provides realistic sample data without requiring a real GCP account.
When you get GCP credentials, switch to real_gcp_scanner.py
"""

from typing import List, Dict
import datetime


class MockGCPClient:
    """Simulates GCP API responses with realistic AI workload examples"""
    
    def __init__(self, project_id: str = "mock-shadow-ai-project"):
        self.project_id = project_id
        print(f"🔧 MockGCPClient initialized for project: {project_id}")
    
    def scan_all_resources(self) -> List[Dict]:
        """Scan all GCP resources and return combined list"""
        resources = []
        resources.extend(self.list_cloud_run_services())
        resources.extend(self.list_cloud_functions())
        resources.extend(self.list_gke_workloads())
        resources.extend(self.list_vertex_ai_endpoints())
        return resources
    
    def list_cloud_run_services(self) -> List[Dict]:
        """Mock Cloud Run services with varying AI confidence levels"""
        timestamp = datetime.datetime.utcnow().isoformat()
        
        return [
            {
                'id': 'cloud-run-001',
                'name': 'ai-chatbot-service',
                'resource_type': 'cloud_run',
                'region': 'us-central1',
                'runtime': 'python311',
                'service_account': 'chatbot-sa@mock-project.iam.gserviceaccount.com',
                'is_public': True,
                'logging_enabled': True,
                'environment': {
                    'OPENAI_API_KEY': 'sk-proj-xxx...xxx',
                    'MODEL': 'gpt-4',
                    'TEMPERATURE': '0.7',
                    'LANGCHAIN_VERSION': '0.1.0',
                    'LANGCHAIN_API_KEY': 'lc-xxx...xxx',
                    'MAX_TOKENS': '2000',
                },
                'labels': {
                    'app': 'chatbot',
                    'ai-enabled': 'true',
                    'team': 'ml-ops',
                    'framework': 'langchain'
                },
                'dependencies': [
                    'langchain==0.1.0',
                    'openai==1.12.0',
                    'fastapi==0.109.0'
                ],
                'discovered_at': timestamp,
            },
            {
                'id': 'cloud-run-002',
                'name': 'document-processor',
                'resource_type': 'cloud_run',
                'region': 'us-east1',
                'runtime': 'python39',
                'service_account': 'processor-sa@mock-project.iam.gserviceaccount.com',
                'is_public': False,
                'logging_enabled': True,
                'environment': {
                    'ANTHROPIC_API_KEY': 'sk-ant-xxx...xxx',
                    'LLAMAINDEX_VERSION': '0.9.48',
                    'MODEL_NAME': 'claude-3-opus',
                    'EMBEDDING_MODEL': 'text-embedding-ada-002',
                    'CHROMADB_HOST': 'localhost',
                },
                'labels': {
                    'app': 'document-ai',
                    'type': 'ai-processor',
                    'team': 'data-science'
                },
                'dependencies': [
                    'llama-index==0.9.48',
                    'anthropic==0.18.0',
                    'chromadb==0.4.22'
                ],
                'discovered_at': timestamp,
            },
            {
                'id': 'cloud-run-003',
                'name': 'web-frontend',
                'resource_type': 'cloud_run',
                'region': 'us-west1',
                'runtime': 'nodejs20',
                'service_account': 'frontend-sa@mock-project.iam.gserviceaccount.com',
                'is_public': True,
                'logging_enabled': True,
                'environment': {
                    'NODE_ENV': 'production',
                    'API_URL': 'https://api.example.com',
                    'PORT': '8080',
                },
                'labels': {
                    'app': 'frontend',
                    'team': 'web',
                    'tier': 'presentation'
                },
                'dependencies': [],
                'discovered_at': timestamp,
            },
            {
                'id': 'cloud-run-004',
                'name': 'vertex-ai-pipeline',
                'resource_type': 'cloud_run',
                'region': 'us-central1',
                'runtime': 'python311',
                'service_account': 'vertex-pipeline@mock-project.iam.gserviceaccount.com',
                'is_public': False,
                'logging_enabled': True,
                'environment': {
                    'VERTEX_AI_ENDPOINT': 'us-central1-aiplatform.googleapis.com',
                    'GOOGLE_AI_KEY': 'AIza...xxx',
                    'MODEL_ID': 'gemini-1.5-pro',
                    'LANGCHAIN_TRACING': 'true',
                    'PROJECT_ID': self.project_id,
                },
                'labels': {
                    'ai-enabled': 'true',
                    'framework': 'langchain',
                    'provider': 'vertex-ai',
                    'ml': 'true'
                },
                'dependencies': [
                    'google-cloud-aiplatform==1.38.0',
                    'langchain==0.1.5',
                    'langchain-google-vertexai==0.0.5'
                ],
                'discovered_at': timestamp,
            },
        ]
    
    def list_cloud_functions(self) -> List[Dict]:
        """Mock Cloud Functions"""
        timestamp = datetime.datetime.utcnow().isoformat()
        
        return [
            {
                'id': 'cloud-function-001',
                'name': 'intelligent-summarizer',
                'resource_type': 'cloud_function',
                'region': 'us-central1',
                'runtime': 'python39',
                'service_account': 'summarizer@mock-project.iam.gserviceaccount.com',
                'is_public': False,
                'logging_enabled': True,
                'environment': {
                    'COHERE_API_KEY': 'co-xxx...xxx',
                    'MODEL': 'command-r-plus',
                    'LANGCHAIN_VERSION': '0.1.0'
                },
                'labels': {
                    'function': 'summarization',
                    'ai': 'true',
                    'team': 'nlp'
                },
                'dependencies': [
                    'cohere==4.47',
                    'langchain==0.1.0'
                ],
                'discovered_at': timestamp,
            },
            {
                'id': 'cloud-function-002',
                'name': 'send-notification',
                'resource_type': 'cloud_function',
                'region': 'us-east1',
                'runtime': 'python39',
                'service_account': 'notifier@mock-project.iam.gserviceaccount.com',
                'is_public': False,
                'logging_enabled': True,
                'environment': {
                    'SENDGRID_API_KEY': 'SG.xxx...xxx',
                    'SMTP_HOST': 'smtp.sendgrid.net',
                    'FROM_EMAIL': 'noreply@example.com'
                },
                'labels': {
                    'function': 'notification',
                    'team': 'platform'
                },
                'dependencies': [
                    'sendgrid==6.11.0',
                    'flask==3.0.0'
                ],
                'discovered_at': timestamp,
            },
            {
                'id': 'cloud-function-003',
                'name': 'embedding-generator',
                'resource_type': 'cloud_function',
                'region': 'us-west1',
                'runtime': 'python311',
                'service_account': 'embeddings@mock-project.iam.gserviceaccount.com',
                'is_public': False,
                'logging_enabled': True,
                'environment': {
                    'OPENAI_API_KEY': 'sk-proj-xxx...xxx',
                    'EMBEDDING_MODEL': 'text-embedding-3-small',
                    'BATCH_SIZE': '100',
                    'PINECONE_API_KEY': 'pc-xxx...xxx',
                    'PINECONE_ENV': 'us-west1-gcp'
                },
                'labels': {
                    'function': 'embeddings',
                    'llm': 'true',
                    'vector-db': 'pinecone'
                },
                'dependencies': [
                    'openai==1.12.0',
                    'pinecone-client==3.0.0',
                    'sentence-transformers==2.3.1'
                ],
                'discovered_at': timestamp,
            },
        ]
    
    def list_gke_workloads(self) -> List[Dict]:
        """Mock GKE workloads"""
        timestamp = datetime.datetime.utcnow().isoformat()
        
        return [
            {
                'id': 'gke-001',
                'name': 'crewai-agents-deployment',
                'resource_type': 'gke',
                'cluster': 'production-cluster',
                'namespace': 'ai-workloads',
                'region': 'us-central1',
                'runtime': 'python311',
                'service_account': 'crewai-admin@mock-project.iam.gserviceaccount.com',
                'is_public': True,
                'logging_enabled': False,  # Risk factor!
                'environment': {
                    'OPENAI_API_KEY': 'sk-proj-xxx...xxx',
                    'ANTHROPIC_API_KEY': 'sk-ant-xxx...xxx',
                    'CREWAI_VERSION': '0.2.0',
                    'LANGCHAIN_API_KEY': 'lc-xxx...xxx',
                    'LANGGRAPH_VERSION': '0.0.40',
                    'MODEL': 'gpt-4-turbo',
                },
                'labels': {
                    'framework': 'crewai',
                    'ai-agent': 'true',
                    'multi-agent': 'true',
                    'team': 'ai-research'
                },
                'dependencies': [
                    'crewai==0.2.0',
                    'langchain==0.1.5',
                    'langgraph==0.0.40',
                    'openai==1.12.0',
                    'anthropic==0.18.0'
                ],
                'discovered_at': timestamp,
            },
            {
                'id': 'gke-002',
                'name': 'nginx-ingress',
                'resource_type': 'gke',
                'cluster': 'production-cluster',
                'namespace': 'ingress-nginx',
                'region': 'us-central1',
                'runtime': 'nginx',
                'service_account': 'nginx@mock-project.iam.gserviceaccount.com',
                'is_public': True,
                'logging_enabled': True,
                'environment': {
                    'NGINX_VERSION': '1.21',
                    'SSL_PROTOCOLS': 'TLSv1.2 TLSv1.3'
                },
                'labels': {
                    'app': 'ingress',
                    'component': 'nginx'
                },
                'dependencies': [],
                'discovered_at': timestamp,
            },
            {
                'id': 'gke-003',
                'name': 'autogen-studio',
                'resource_type': 'gke',
                'cluster': 'dev-cluster',
                'namespace': 'experiments',
                'region': 'us-west1',
                'runtime': 'python311',
                'service_account': 'autogen-dev@mock-project.iam.gserviceaccount.com',
                'is_public': False,
                'logging_enabled': True,
                'environment': {
                    'OPENAI_API_KEY': 'sk-proj-xxx...xxx',
                    'AUTOGEN_VERSION': '0.2.0',
                    'MODEL': 'gpt-4',
                    'TEMPERATURE': '0.8',
                },
                'labels': {
                    'framework': 'autogen',
                    'ai-agent': 'true',
                    'env': 'dev'
                },
                'dependencies': [
                    'pyautogen==0.2.0',
                    'openai==1.12.0'
                ],
                'discovered_at': timestamp,
            },
        ]
    
    def list_vertex_ai_endpoints(self) -> List[Dict]:
        """Mock Vertex AI endpoints"""
        timestamp = datetime.datetime.utcnow().isoformat()
        
        return [
            {
                'id': 'vertex-001',
                'name': 'custom-llm-endpoint',
                'resource_type': 'vertex_ai',
                'region': 'us-central1',
                'runtime': 'vertex-ai',
                'service_account': 'vertex-endpoint@mock-project.iam.gserviceaccount.com',
                'is_public': False,
                'logging_enabled': True,
                'environment': {
                    'MODEL_ID': 'text-bison@002',
                    'ENDPOINT_ID': 'projects/mock-project/locations/us-central1/endpoints/123456'
                },
                'labels': {
                    'model-type': 'llm',
                    'provider': 'vertex-ai',
                    'ai-enabled': 'true'
                },
                'dependencies': [
                    'google-cloud-aiplatform==1.38.0'
                ],
                'discovered_at': timestamp,
            },
            {
                'id': 'vertex-002',
                'name': 'gemini-pro-endpoint',
                'resource_type': 'vertex_ai',
                'region': 'us-central1',
                'runtime': 'vertex-ai',
                'service_account': 'gemini-sa@mock-project.iam.gserviceaccount.com',
                'is_public': False,
                'logging_enabled': True,
                'environment': {
                    'MODEL_ID': 'gemini-1.5-pro-preview',
                    'VERTEX_AI_ENDPOINT': 'us-central1-aiplatform.googleapis.com'
                },
                'labels': {
                    'model': 'gemini',
                    'model-type': 'multimodal-llm',
                    'ai': 'true'
                },
                'dependencies': [
                    'google-generativeai==0.3.2',
                    'google-cloud-aiplatform==1.38.0'
                ],
                'discovered_at': timestamp,
            },
        ]
    
    def get_project_info(self) -> Dict:
        """Get mock project information"""
        return {
            'project_id': self.project_id,
            'project_name': 'Shadow AI Test Project',
            'project_number': '123456789',
            'state': 'ACTIVE',
            'create_time': '2024-01-15T10:00:00Z'
        }
