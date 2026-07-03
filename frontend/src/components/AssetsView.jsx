import { useState, useEffect } from 'react';
import apiService from '../services/api';

export default function AssetsView() {
  const [assets, setAssets] = useState([]);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAssets();
  }, [filter]);

  const loadAssets = async () => {
    setLoading(true);
    try {
      const data = await apiService.getAssets(filter === 'all' ? null : filter);
      setAssets(data.assets);
    } catch (error) {
      console.error('Failed to load assets:', error);
    }
    setLoading(false);
  };

  const resourceTypes = [
    { value: 'all', label: 'All Resources' },
    { value: 'cloud_run', label: 'Cloud Run' },
    { value: 'cloud_function', label: 'Cloud Functions' },
    { value: 'gke', label: 'GKE' },
    { value: 'vertex_ai', label: 'Vertex AI' },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-gray-500">Loading assets...</div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900">Assets</h2>
        <p className="text-gray-500 mt-1">All discovered cloud resources</p>
      </div>

      {/* Filter */}
      <div className="mb-6 flex flex-wrap gap-2">
        {resourceTypes.map((type) => (
          <button
            key={type.value}
            onClick={() => setFilter(type.value)}
            className={`px-4 py-2 rounded-lg font-medium ${
              filter === type.value
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
            }`}
          >
            {type.label}
          </button>
        ))}
      </div>

      {/* Assets Grid */}
      {assets.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <p className="text-gray-500">No assets found</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {assets.map((asset) => (
            <AssetCard key={asset.id} asset={asset} />
          ))}
        </div>
      )}
    </div>
  );
}

function AssetCard({ asset }) {
  const typeColors = {
    cloud_run: 'bg-blue-100 text-blue-800',
    cloud_function: 'bg-green-100 text-green-800',
    gke: 'bg-purple-100 text-purple-800',
    vertex_ai: 'bg-orange-100 text-orange-800',
  };

  const typeColor = typeColors[asset.resource_type] || 'bg-gray-100 text-gray-800';

  return (
    <div className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-semibold text-gray-900 truncate">
            {asset.name}
          </h3>
          <p className="text-sm text-gray-500 mt-1">{asset.region}</p>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-medium ${typeColor}`}>
          {asset.resource_type.replace('_', ' ')}
        </span>
      </div>

      {/* Details */}
      <div className="space-y-2 mb-4">
        {asset.runtime && (
          <div className="flex items-center text-sm">
            <span className="text-gray-500 w-20">Runtime:</span>
            <span className="text-gray-900 font-medium">{asset.runtime}</span>
          </div>
        )}
        {asset.service_account && (
          <div className="flex items-start text-sm">
            <span className="text-gray-500 w-20 flex-shrink-0">SA:</span>
            <span className="text-gray-900 font-mono text-xs break-all">
              {asset.service_account.split('@')[0]}
            </span>
          </div>
        )}
      </div>

      {/* Labels */}
      {asset.labels && Object.keys(asset.labels).length > 0 && (
        <div className="flex flex-wrap gap-2 mb-3">
          {Object.entries(asset.labels).slice(0, 3).map(([key, value]) => (
            <span
              key={key}
              className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs"
            >
              {key}={value}
            </span>
          ))}
          {Object.keys(asset.labels).length > 3 && (
            <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
              +{Object.keys(asset.labels).length - 3} more
            </span>
          )}
        </div>
      )}

      {/* Footer */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <div className="flex items-center space-x-3 text-xs text-gray-500">
          {asset.is_public && (
            <span className="flex items-center text-orange-600">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 2a8 8 0 100 16 8 8 0 000-16zm1 11H9v-2h2v2zm0-4H9V5h2v4z" />
              </svg>
              Public
            </span>
          )}
          {!asset.logging_enabled && (
            <span className="flex items-center text-red-600">
              No Logging
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
