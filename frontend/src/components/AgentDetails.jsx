import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import apiService from '../services/api';

export default function AgentDetails() {
  const { agentId } = useParams();
  const navigate = useNavigate();
  const [agent, setAgent] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAgent();
  }, [agentId]);

  const loadAgent = async () => {
    setLoading(true);
    try {
      const data = await apiService.getAgent(agentId);
      setAgent(data);
    } catch (error) {
      console.error('Failed to load agent:', error);
    }
    setLoading(false);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-gray-500">Loading agent details...</div>
      </div>
    );
  }

  if (!agent) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-red-500">Agent not found</div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back Button */}
      <button
        onClick={() => navigate('/agents')}
        className="mb-6 flex items-center text-gray-600 hover:text-gray-900"
      >
        <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
          <path
            fillRule="evenodd"
            d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
            clipRule="evenodd"
          />
        </svg>
        Back to Agents
      </button>

      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{agent.asset.name}</h1>
            <p className="text-gray-500 mt-1">{agent.asset.region}</p>
          </div>
          <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
            {agent.asset.resource_type}
          </span>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
          <StatBox label="Confidence" value={`${agent.confidence_score}%`} color="green" />
          <StatBox label="Risk Score" value={agent.risk_score} color={agent.risk_score > 50 ? 'red' : 'yellow'} />
          <StatBox label="Indicators" value={agent.indicators.length} color="blue" />
          <StatBox label="Runtime" value={agent.asset.runtime || 'N/A'} color="gray" />
        </div>
      </div>

      {/* Confidence Scoring Breakdown */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Confidence Score Breakdown
        </h2>
        <div className="space-y-4">
          {agent.reasons.map((reason, idx) => (
            <ReasonCard key={idx} reason={reason} />
          ))}
        </div>
      </div>

      {/* Risk Assessment */}
      {agent.risk_factors && agent.risk_factors.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Risk Assessment
          </h2>
          <div className="space-y-4">
            {agent.risk_factors.map((risk, idx) => (
              <RiskCard key={idx} risk={risk} />
            ))}
          </div>
        </div>
      )}

      {/* Detected Indicators */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Detected Indicators
        </h2>
        <div className="flex flex-wrap gap-2">
          {agent.indicators.map((indicator, idx) => (
            <span
              key={idx}
              className="px-3 py-2 bg-indigo-100 text-indigo-800 rounded-lg text-sm font-medium"
            >
              {indicator}
            </span>
          ))}
        </div>
      </div>

      {/* Environment Variables */}
      {agent.asset.environment && Object.keys(agent.asset.environment).length > 0 && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Environment Variables
          </h2>
          <div className="bg-gray-50 rounded-lg p-4 font-mono text-sm">
            {Object.entries(agent.asset.environment).map(([key, value]) => (
              <div key={key} className="py-1">
                <span className="text-indigo-600">{key}</span>
                <span className="text-gray-500">=</span>
                <span className="text-gray-700">{maskSensitiveValue(key, value)}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Resource Metadata */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Resource Metadata
        </h2>
        <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <MetadataRow label="Resource ID" value={agent.asset.id} />
          <MetadataRow label="Resource Type" value={agent.asset.resource_type} />
          <MetadataRow label="Region" value={agent.asset.region} />
          <MetadataRow label="Runtime" value={agent.asset.runtime} />
          <MetadataRow label="Service Account" value={agent.asset.service_account} mono />
          <MetadataRow
            label="Public Access"
            value={agent.asset.is_public ? 'Yes' : 'No'}
            color={agent.asset.is_public ? 'text-orange-600' : 'text-green-600'}
          />
          <MetadataRow
            label="Logging Enabled"
            value={agent.asset.logging_enabled ? 'Yes' : 'No'}
            color={agent.asset.logging_enabled ? 'text-green-600' : 'text-red-600'}
          />
          <MetadataRow label="Discovered At" value={new Date(agent.asset.discovered_at).toLocaleString()} />
        </dl>

        {/* Labels */}
        {agent.asset.labels && Object.keys(agent.asset.labels).length > 0 && (
          <div className="mt-6">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Labels</h3>
            <div className="flex flex-wrap gap-2">
              {Object.entries(agent.asset.labels).map(([key, value]) => (
                <span
                  key={key}
                  className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs font-mono"
                >
                  {key}={value}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Dependencies */}
        {agent.asset.dependencies && agent.asset.dependencies.length > 0 && (
          <div className="mt-6">
            <h3 className="text-sm font-medium text-gray-500 mb-2">Dependencies</h3>
            <div className="bg-gray-50 rounded p-3 font-mono text-xs space-y-1">
              {agent.asset.dependencies.map((dep, idx) => (
                <div key={idx} className="text-gray-700">{dep}</div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function StatBox({ label, value, color }) {
  const colors = {
    green: 'bg-green-50 text-green-700 border-green-200',
    red: 'bg-red-50 text-red-700 border-red-200',
    yellow: 'bg-yellow-50 text-yellow-700 border-yellow-200',
    blue: 'bg-blue-50 text-blue-700 border-blue-200',
    gray: 'bg-gray-50 text-gray-700 border-gray-200',
  };

  return (
    <div className={`p-4 rounded-lg border ${colors[color]}`}>
      <div className="text-2xl font-bold">{value}</div>
      <div className="text-sm opacity-75">{label}</div>
    </div>
  );
}

function ReasonCard({ reason }) {
  const severityColors = {
    high: 'border-red-500 bg-red-50',
    medium: 'border-yellow-500 bg-yellow-50',
    low: 'border-blue-500 bg-blue-50',
  };

  return (
    <div className={`border-l-4 p-4 rounded-r ${severityColors[reason.severity]}`}>
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-semibold text-gray-900">{reason.category}</h3>
        <span className="text-green-600 font-bold">{reason.confidence_impact}</span>
      </div>
      <p className="text-gray-700 text-sm">{reason.finding}</p>
      <span className="text-xs text-gray-500 capitalize mt-1 inline-block">
        {reason.severity} severity
      </span>
    </div>
  );
}

function RiskCard({ risk }) {
  const severityColors = {
    high: 'border-red-500 bg-red-50',
    medium: 'border-yellow-500 bg-yellow-50',
    low: 'border-blue-500 bg-blue-50',
  };

  return (
    <div className={`border-l-4 p-4 rounded-r ${severityColors[risk.severity]}`}>
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-semibold text-gray-900">{risk.factor}</h3>
        <span className="text-red-600 font-bold">{risk.impact}</span>
      </div>
      <p className="text-gray-700 text-sm">{risk.description}</p>
      <span className="text-xs text-gray-500 capitalize mt-1 inline-block">
        {risk.severity} severity
      </span>
    </div>
  );
}

function MetadataRow({ label, value, mono = false, color = 'text-gray-900' }) {
  return (
    <div>
      <dt className="text-sm font-medium text-gray-500">{label}</dt>
      <dd className={`mt-1 text-sm ${color} ${mono ? 'font-mono text-xs break-all' : ''}`}>
        {value || 'N/A'}
      </dd>
    </div>
  );
}

function maskSensitiveValue(key, value) {
  const sensitiveKeys = ['key', 'secret', 'token', 'password', 'api_key'];
  const isSensitive = sensitiveKeys.some(k => key.toLowerCase().includes(k));
  
  if (isSensitive && value && value.length > 8) {
    return value.substring(0, 8) + '...***';
  }
  
  return value;
}
