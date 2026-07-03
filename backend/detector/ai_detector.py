"""
AI Detector - Identifies AI workloads and calculates confidence scores

This module analyzes GCP resources to determine if they're AI-powered agents.
Uses multiple heuristics with weighted scoring for accurate detection.
"""

from typing import Dict, List, Tuple
import re


class AIDetector:
    """Detects AI agents in cloud workloads with confidence scoring"""
    
    # Detection patterns for environment variables
    AI_ENV_PATTERNS = {
        'llm_api_keys': [
            'OPENAI_API_KEY', 'OPENAI_KEY', 'OPENAI_SECRET',
            'ANTHROPIC_API_KEY', 'ANTHROPIC_KEY',
            'GEMINI_API_KEY', 'GOOGLE_AI_KEY',
            'COHERE_API_KEY', 'COHERE_KEY',
            'HUGGINGFACE_TOKEN', 'HF_TOKEN',
        ],
        'ai_frameworks': [
            'LANGCHAIN', 'LANGCHAIN_API_KEY', 'LANGCHAIN_VERSION',
            'LLAMAINDEX', 'LLAMA_INDEX',
            'CREWAI', 'AUTOGEN',
            'LANGGRAPH',
        ],
        'ai_config': [
            'MODEL', 'MODEL_NAME', 'LLM_MODEL',
            'TEMPERATURE', 'MAX_TOKENS',
            'EMBEDDING_MODEL',
        ]
    }
    
    # Detection patterns for labels
    AI_LABEL_PATTERNS = [
        'ai', 'ai-enabled', 'ai-agent',
        'llm', 'language-model',
        'ml', 'machine-learning',
        'langchain', 'llamaindex', 'crewai',
        'chatbot', 'assistant',
    ]
    
    # AI libraries in container images or runtimes
    AI_LIBRARIES = [
        'langchain', 'langchain-core', 'langchain-community',
        'llamaindex', 'llama-index',
        'openai', 'anthropic', 'cohere',
        'transformers', 'sentence-transformers',
        'chromadb', 'pinecone-client', 'weaviate-client',
        'crewai', 'autogen', 'langgraph',
        'google-generativeai', 'vertexai',
    ]
    
    def detect_ai_workload(self, resource: Dict) -> Tuple[bool, int, List[str], List[Dict]]:
        """
        Detect if a resource is an AI workload
        
        Args:
            resource: Resource metadata from GCP scanner
            
        Returns:
            Tuple of (is_ai_agent, confidence_score, indicators, reasons)
        """
        indicators = []
        reasons = []
        score = 0
        
        # 1. Check environment variables for LLM API keys (HIGH confidence)
        env_vars = resource.get('environment', {})
        llm_keys_found = self._check_llm_api_keys(env_vars)
        if llm_keys_found:
            key_count = len(llm_keys_found)
            # Each LLM key is strong evidence (+30 points)
            points = min(key_count * 30, 50)  # Cap at 50 for multiple keys
            score += points
            indicators.extend(llm_keys_found)
            reasons.append({
                'category': 'LLM API Keys',
                'finding': f"Found {key_count} LLM API key(s): {', '.join(llm_keys_found)}",
                'confidence_impact': f'+{points}',
                'severity': 'high'
            })
        
        # 2. Check for AI framework environment variables (HIGH confidence)
        frameworks_found = self._check_ai_frameworks(env_vars)
        if frameworks_found:
            points = len(frameworks_found) * 25
            score += points
            indicators.extend(frameworks_found)
            reasons.append({
                'category': 'AI Frameworks',
                'finding': f"Detected framework(s): {', '.join(frameworks_found)}",
                'confidence_impact': f'+{points}',
                'severity': 'high'
            })
        
        # 3. Check for AI-related labels (MEDIUM confidence)
        labels = resource.get('labels', {})
        ai_labels = self._check_ai_labels(labels)
        if ai_labels:
            points = min(len(ai_labels) * 15, 30)  # Cap at 30
            score += points
            indicators.extend([f"label:{label}" for label in ai_labels])
            reasons.append({
                'category': 'Resource Labels',
                'finding': f"AI-related labels: {', '.join(ai_labels)}",
                'confidence_impact': f'+{points}',
                'severity': 'medium'
            })
        
        # 4. Check for Vertex AI usage (HIGH confidence)
        if self._check_vertex_ai_usage(resource):
            score += 25
            indicators.append('vertex_ai')
            reasons.append({
                'category': 'Vertex AI Integration',
                'finding': 'Uses Google Vertex AI services',
                'confidence_impact': '+25',
                'severity': 'high'
            })
        
        # 5. Check runtime and dependencies (MEDIUM confidence)
        libraries_found = self._check_ai_libraries(resource)
        if libraries_found:
            points = min(len(libraries_found) * 10, 30)  # Cap at 30
            score += points
            indicators.extend([f"lib:{lib}" for lib in libraries_found])
            reasons.append({
                'category': 'AI Libraries',
                'finding': f"Detected libraries: {', '.join(libraries_found[:5])}{'...' if len(libraries_found) > 5 else ''}",
                'confidence_impact': f'+{points}',
                'severity': 'medium'
            })
        
        # 6. Check for AI-related configuration (LOW confidence)
        ai_config = self._check_ai_config(env_vars)
        if ai_config:
            points = min(len(ai_config) * 5, 15)  # Cap at 15
            score += points
            indicators.extend([f"config:{cfg}" for cfg in ai_config])
            reasons.append({
                'category': 'AI Configuration',
                'finding': f"AI config detected: {', '.join(ai_config)}",
                'confidence_impact': f'+{points}',
                'severity': 'low'
            })
        
        # 7. Check service account permissions (MEDIUM confidence)
        if self._check_ai_permissions(resource):
            score += 15
            indicators.append('ai_permissions')
            reasons.append({
                'category': 'IAM Permissions',
                'finding': 'Service account has AI/ML permissions',
                'confidence_impact': '+15',
                'severity': 'medium'
            })
        
        # Cap confidence at 100
        confidence = min(score, 100)
        
        # Determine if it's an AI agent (threshold: 30% confidence)
        is_ai_agent = confidence >= 30
        
        return is_ai_agent, confidence, indicators, reasons
    
    def _check_llm_api_keys(self, env_vars: Dict) -> List[str]:
        """Check for LLM API keys in environment variables"""
        found = []
        for key in env_vars.keys():
            key_upper = key.upper()
            for pattern in self.AI_ENV_PATTERNS['llm_api_keys']:
                if pattern in key_upper:
                    found.append(key)
                    break
        return found
    
    def _check_ai_frameworks(self, env_vars: Dict) -> List[str]:
        """Check for AI framework indicators in environment variables"""
        found = []
        for key in env_vars.keys():
            key_upper = key.upper()
            for pattern in self.AI_ENV_PATTERNS['ai_frameworks']:
                if pattern in key_upper:
                    # Extract framework name
                    if 'LANGCHAIN' in key_upper:
                        framework = 'LangChain'
                    elif 'LLAMAINDEX' in key_upper or 'LLAMA_INDEX' in key_upper:
                        framework = 'LlamaIndex'
                    elif 'CREWAI' in key_upper:
                        framework = 'CrewAI'
                    elif 'AUTOGEN' in key_upper:
                        framework = 'AutoGen'
                    elif 'LANGGRAPH' in key_upper:
                        framework = 'LangGraph'
                    else:
                        framework = key
                    if framework not in found:
                        found.append(framework)
                    break
        return found
    
    def _check_ai_labels(self, labels: Dict) -> List[str]:
        """Check for AI-related labels"""
        found = []
        for key, value in labels.items():
            combined = f"{key}:{value}".lower()
            for pattern in self.AI_LABEL_PATTERNS:
                if pattern in combined or pattern in key.lower():
                    found.append(f"{key}={value}")
                    break
        return found
    
    def _check_vertex_ai_usage(self, resource: Dict) -> bool:
        """Check if resource uses Vertex AI"""
        # Check environment variables
        env_vars = resource.get('environment', {})
        vertex_indicators = ['VERTEX', 'GOOGLE_AI', 'GEMINI', 'AIPLATFORM']
        for key in env_vars.keys():
            if any(indicator in key.upper() for indicator in vertex_indicators):
                return True
        
        # Check service account
        sa = resource.get('service_account', '')
        if 'aiplatform' in sa or 'vertex' in sa:
            return True
        
        # Check resource metadata
        if resource.get('resource_type') == 'vertex_ai':
            return True
        
        return False
    
    def _check_ai_libraries(self, resource: Dict) -> List[str]:
        """Check for AI libraries in dependencies or container images"""
        found = []
        
        # Check environment for library versions (indicates installation)
        env_vars = resource.get('environment', {})
        for key, value in env_vars.items():
            key_lower = key.lower()
            for lib in self.AI_LIBRARIES:
                if lib.lower() in key_lower or lib.lower() in str(value).lower():
                    if lib not in found:
                        found.append(lib)
        
        # Check runtime description
        runtime = resource.get('runtime', '').lower()
        for lib in self.AI_LIBRARIES:
            if lib.lower() in runtime:
                if lib not in found:
                    found.append(lib)
        
        # Check dependencies field if available
        dependencies = resource.get('dependencies', [])
        for dep in dependencies:
            dep_lower = dep.lower()
            for lib in self.AI_LIBRARIES:
                if lib.lower() in dep_lower:
                    if lib not in found:
                        found.append(lib)
        
        return found
    
    def _check_ai_config(self, env_vars: Dict) -> List[str]:
        """Check for AI-related configuration variables"""
        found = []
        for key in env_vars.keys():
            key_upper = key.upper()
            for pattern in self.AI_ENV_PATTERNS['ai_config']:
                if pattern in key_upper:
                    found.append(key)
                    break
        return found
    
    def _check_ai_permissions(self, resource: Dict) -> bool:
        """Check if service account has AI/ML permissions"""
        sa = resource.get('service_account', '')
        ai_sa_patterns = [
            'aiplatform', 'vertex', 'ml-', 'ai-',
            'genai', 'llm', 'model'
        ]
        return any(pattern in sa.lower() for pattern in ai_sa_patterns)
    
    def calculate_risk_score(self, resource: Dict, confidence: int, indicators: List[str]) -> Tuple[int, List[Dict]]:
        """
        Calculate security risk score for an AI agent
        
        Returns:
            Tuple of (risk_score, risk_factors)
        """
        risk_score = 0
        risk_factors = []
        
        # High risk: External LLM usage (data leaving GCP)
        external_llm_keys = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'COHERE_API_KEY']
        env_vars = resource.get('environment', {})
        if any(key in env_vars for key in external_llm_keys):
            risk_score += 30
            risk_factors.append({
                'factor': 'External LLM Usage',
                'description': 'Data may be sent to external AI providers',
                'impact': '+30',
                'severity': 'high'
            })
        
        # High risk: Public endpoint
        if resource.get('is_public', False):
            risk_score += 20
            risk_factors.append({
                'factor': 'Public Endpoint',
                'description': 'Service is publicly accessible',
                'impact': '+20',
                'severity': 'high'
            })
        
        # Medium risk: Privileged service account
        sa = resource.get('service_account', '')
        if 'admin' in sa.lower() or 'owner' in sa.lower():
            risk_score += 20
            risk_factors.append({
                'factor': 'Privileged Service Account',
                'description': 'Uses admin/owner service account',
                'impact': '+20',
                'severity': 'high'
            })
        
        # Medium risk: No logging/monitoring
        if not resource.get('logging_enabled', True):
            risk_score += 10
            risk_factors.append({
                'factor': 'Logging Disabled',
                'description': 'Activity monitoring is not enabled',
                'impact': '+10',
                'severity': 'medium'
            })
        
        # Low risk: Multiple AI services (complexity)
        if len(indicators) > 5:
            risk_score += 10
            risk_factors.append({
                'factor': 'Complex AI Stack',
                'description': f'Uses {len(indicators)} different AI components',
                'impact': '+10',
                'severity': 'low'
            })
        
        return min(risk_score, 100), risk_factors


# Convenience function
def detect_ai_agent(resource: Dict) -> Dict:
    """
    Detect AI agent and return full analysis
    
    Returns:
        Dict with: is_ai, confidence, indicators, reasons, risk_score, risk_factors
    """
    detector = AIDetector()
    is_ai, confidence, indicators, reasons = detector.detect_ai_workload(resource)
    
    result = {
        'is_ai_agent': is_ai,
        'confidence_score': confidence,
        'indicators': indicators,
        'reasons': reasons,
    }
    
    # Calculate risk if it's an AI agent
    if is_ai:
        risk_score, risk_factors = detector.calculate_risk_score(resource, confidence, indicators)
        result['risk_score'] = risk_score
        result['risk_factors'] = risk_factors
    else:
        result['risk_score'] = 0
        result['risk_factors'] = []
    
    return result
