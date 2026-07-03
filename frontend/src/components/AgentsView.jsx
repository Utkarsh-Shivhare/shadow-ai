import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiService from '../services/api';

export default function AgentsView() {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadAgents();
  }, []);

  const loadAgents = async () => {
    setLoading(true);
    try {
      const data = await apiService.getAgents();
      setAgents(data.agents);
    } catch (error) {
      console.error('Failed to load agents:', error);
    }
    setLoading(false);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-gray-500">Loading agents...</div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900">AI Agents</h2>
        <p className="text-gray-500 mt-1">
          Detected AI workloads with confidence scores
        </p>
      </div>

      {agents.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <p className="text-gray-500">No AI agents detected</p>
          <p className="text-sm text-gray-400 mt-2">
            Try running a scan to discover AI workloads
          </p>
        </div>
      ) : (
        <div className="bg-white shadow rounded-lg overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Region
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Confidence
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Risk
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Indicators
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {agents.map((agent) => (
                <tr
                  key={agent.id}
                  className="hover:bg-gray-50 cursor-pointer"
                  onClick={() => navigate(`/agents/${agent.id}`)}
                >
                  <td className="px-6 py-4">
                    <div className="text-sm font-medium text-gray-900">
                      {agent.name}
                    </div>
                    <div className="text-sm text-gray-500">{agent.runtime}</div>
                  </td>
                  <td className="px-6 py-4">
                    <span className="px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800">
                      {agent.resource_type}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {agent.region}
                  </td>
                  <td className="px-6 py-4">
                    <ConfidenceBadge score={agent.confidence_score} />
                  </td>
                  <td className="px-6 py-4">
                    <RiskBadge score={agent.risk_score} />
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex flex-wrap gap-1">
                      {agent.indicators.slice(0, 3).map((indicator, idx) => (
                        <span
                          key={idx}
                          className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded"
                        >
                          {indicator}
                        </span>
                      ))}
                      {agent.indicators.length > 3 && (
                        <span className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded">
                          +{agent.indicators.length - 3}
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-right text-sm font-medium">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        navigate(`/agents/${agent.id}`);
                      }}
                      className="text-indigo-600 hover:text-indigo-900"
                    >
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

function ConfidenceBadge({ score }) {
  let color = 'bg-gray-100 text-gray-800';
  if (score >= 80) color = 'bg-green-100 text-green-800';
  else if (score >= 60) color = 'bg-yellow-100 text-yellow-800';
  else if (score >= 40) color = 'bg-orange-100 text-orange-800';
  else color = 'bg-red-100 text-red-800';

  return (
    <div className="flex items-center">
      <div className="flex-1 max-w-32 mr-2">
        <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
          <div
            className={`h-full ${color}`}
            style={{ width: `${score}%` }}
          ></div>
        </div>
      </div>
      <span className={`px-2 py-1 text-xs font-medium rounded ${color}`}>
        {score}%
      </span>
    </div>
  );
}

function RiskBadge({ score }) {
  if (score === 0) {
    return <span className="px-2 py-1 text-xs font-medium rounded bg-green-100 text-green-800">Low</span>;
  } else if (score < 40) {
    return <span className="px-2 py-1 text-xs font-medium rounded bg-yellow-100 text-yellow-800">Medium</span>;
  } else if (score < 70) {
    return <span className="px-2 py-1 text-xs font-medium rounded bg-orange-100 text-orange-800">High</span>;
  } else {
    return <span className="px-2 py-1 text-xs font-medium rounded bg-red-100 text-red-800">Critical</span>;
  }
}
