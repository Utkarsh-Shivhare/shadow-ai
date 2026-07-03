import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiService from '../services/api';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [scanning, setScanning] = useState(false);
  const [scanMessage, setScanMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await apiService.getStatistics();
      setStats(data);
    } catch (error) {
      console.error('Failed to load statistics:', error);
    }
  };

  const handleScan = async () => {
    setScanning(true);
    setScanMessage('Scanning GCP project...');
    
    try {
      const result = await apiService.triggerScan();
      setScanMessage(`Scan started successfully! (${result.scan_id})`);
      
      // Wait a bit for scan to complete
      setTimeout(async () => {
        await loadStats();
        setScanMessage('Scan completed! Data refreshed.');
        setScanning(false);
        setTimeout(() => setScanMessage(''), 3000);
      }, 3000);
    } catch (error) {
      setScanMessage('Scan failed: ' + error.message);
      setScanning(false);
    }
  };

  if (!stats) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-gray-500">Loading...</div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header with Scan Button */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Dashboard</h2>
          <p className="text-gray-500 mt-1">Shadow AI workload discovery</p>
        </div>
        <button
          onClick={handleScan}
          disabled={scanning}
          className={`px-6 py-3 rounded-lg font-medium text-white ${
            scanning
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-indigo-600 hover:bg-indigo-700'
          }`}
        >
          {scanning ? 'Scanning...' : 'Scan Project'}
        </button>
      </div>

      {/* Scan Message */}
      {scanMessage && (
        <div className="mb-6 p-4 rounded-lg bg-blue-50 border border-blue-200 text-blue-700">
          {scanMessage}
        </div>
      )}

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Assets"
          value={stats.total_assets}
          subtitle="Cloud resources"
          color="blue"
          onClick={() => navigate('/assets')}
        />
        <StatCard
          title="AI Agents"
          value={stats.total_agents}
          subtitle={stats.detection_rate + ' detection rate'}
          color="indigo"
          onClick={() => navigate('/agents')}
        />
        <StatCard
          title="Avg Confidence"
          value={stats.average_confidence + '%'}
          subtitle="Detection accuracy"
          color="green"
        />
        <StatCard
          title="High Risk"
          value={stats.high_risk_agents}
          subtitle="Risk score > 50"
          color="red"
        />
      </div>

      {/* Assets by Type */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Assets by Type</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(stats.assets_by_type).map(([type, count]) => (
            <div key={type} className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">{count}</div>
              <div className="text-sm text-gray-500 capitalize">
                {type.replace('_', ' ')}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ActionCard
          title="View All Assets"
          description="Browse all discovered cloud resources"
          buttonText="View Assets"
          onClick={() => navigate('/assets')}
        />
        <ActionCard
          title="View AI Agents"
          description="Review detected AI workloads and risk scores"
          buttonText="View Agents"
          onClick={() => navigate('/agents')}
        />
      </div>
    </div>
  );
}

function StatCard({ title, value, subtitle, color, onClick }) {
  const colors = {
    blue: 'bg-blue-500',
    indigo: 'bg-indigo-500',
    green: 'bg-green-500',
    red: 'bg-red-500',
  };

  return (
    <div
      onClick={onClick}
      className={`bg-white rounded-lg shadow p-6 ${onClick ? 'cursor-pointer hover:shadow-lg transition-shadow' : ''}`}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
          <p className="text-sm text-gray-500 mt-1">{subtitle}</p>
        </div>
        <div className={`w-12 h-12 ${colors[color]} rounded-lg opacity-10`}></div>
      </div>
    </div>
  );
}

function ActionCard({ title, description, buttonText, onClick }) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-500 mb-4">{description}</p>
      <button
        onClick={onClick}
        className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 font-medium"
      >
        {buttonText}
      </button>
    </div>
  );
}
