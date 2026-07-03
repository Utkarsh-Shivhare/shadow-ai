import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import AssetsView from './components/AssetsView';
import AgentsView from './components/AgentsView';
import AgentDetails from './components/AgentDetails';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Navigation */}
        <nav className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex">
                <div className="flex-shrink-0 flex items-center">
                  <h1 className="text-xl font-bold text-gray-900">
                    Shadow AI Discovery
                  </h1>
                </div>
                <div className="ml-10 flex space-x-4 items-center">
                  <NavLink
                    to="/"
                    className={({ isActive }) =>
                      `px-3 py-2 rounded-md text-sm font-medium ${
                        isActive
                          ? 'bg-indigo-100 text-indigo-700'
                          : 'text-gray-700 hover:bg-gray-100'
                      }`
                    }
                  >
                    Dashboard
                  </NavLink>
                  <NavLink
                    to="/assets"
                    className={({ isActive }) =>
                      `px-3 py-2 rounded-md text-sm font-medium ${
                        isActive
                          ? 'bg-indigo-100 text-indigo-700'
                          : 'text-gray-700 hover:bg-gray-100'
                      }`
                    }
                  >
                    Assets
                  </NavLink>
                  <NavLink
                    to="/agents"
                    className={({ isActive }) =>
                      `px-3 py-2 rounded-md text-sm font-medium ${
                        isActive
                          ? 'bg-indigo-100 text-indigo-700'
                          : 'text-gray-700 hover:bg-gray-100'
                      }`
                    }
                  >
                    AI Agents
                  </NavLink>
                </div>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/assets" element={<AssetsView />} />
            <Route path="/agents" element={<AgentsView />} />
            <Route path="/agents/:agentId" element={<AgentDetails />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
