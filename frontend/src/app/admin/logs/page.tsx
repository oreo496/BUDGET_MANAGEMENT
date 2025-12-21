'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import MainLayout from '@/components/Layout/MainLayout';
import api from '@/lib/api';
import { 
  DocumentTextIcon,
  FunnelIcon,
  CalendarIcon
} from '@heroicons/react/24/outline';

export default function AdminLogs() {
  const router = useRouter();
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState('all');

  useEffect(() => {
    const adminToken = localStorage.getItem('adminToken');
    if (!adminToken) {
      router.push('/admin/login');
      return;
    }
    fetchLogs();
  }, [router]);

  const fetchLogs = async () => {
    try {
      const res = await api.get('/admin/logs/');
      
      // Handle API response
      const logsData = Array.isArray(res.data) ? res.data : res.data.results || [];
      setLogs(logsData);
    } catch (err: any) {
      if (err?.response?.status === 401 || err?.response?.status === 403) {
        localStorage.removeItem('adminToken');
        localStorage.removeItem('adminEmail');
        router.push('/admin/login');
      }
      console.error('Error fetching logs:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredLogs = filterType === 'all' 
    ? logs 
    : logs.filter(log => log.type === filterType);

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'auth': return 'bg-blue-100 text-blue-800';
      case 'transaction': return 'bg-green-100 text-green-800';
      case 'loan': return 'bg-purple-100 text-purple-800';
      case 'security': return 'bg-red-100 text-red-800';
      case 'admin': return 'bg-orange-100 text-orange-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <MainLayout title="System Logs">
      <div className="space-y-6">
        {/* Header */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
              <DocumentTextIcon className="w-6 h-6 text-purple-600" />
              System Activity Logs
            </h2>
            <button
              onClick={() => alert('Export logs functionality')}
              className="bg-purple-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-purple-700 transition-colors"
            >
              Export Logs
            </button>
          </div>

          {/* Filters */}
          <div className="flex items-center gap-4">
            <FunnelIcon className="w-5 h-5 text-gray-400" />
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="all">All Types</option>
              <option value="auth">Authentication</option>
              <option value="transaction">Transactions</option>
              <option value="loan">Loans</option>
              <option value="security">Security</option>
              <option value="admin">Admin Actions</option>
            </select>
          </div>
        </div>

        {/* Logs List */}
        <div className="bg-white rounded-xl shadow-sm overflow-hidden">
          {loading ? (
            <div className="p-6 text-center text-gray-600">Loading logs...</div>
          ) : filteredLogs.length === 0 ? (
            <div className="p-6 text-center text-gray-600">No logs found</div>
          ) : (
            <div className="divide-y divide-gray-200">
              {filteredLogs.map((log) => (
                <div key={log.id} className="p-6 hover:bg-gray-50 transition-colors">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${getTypeColor(log.type)}`}>
                          {log.type.charAt(0).toUpperCase() + log.type.slice(1)}
                        </span>
                        <h3 className="font-semibold text-gray-800">{log.action}</h3>
                      </div>
                      <p className="text-sm text-gray-600 mb-2">{log.details}</p>
                      <div className="flex items-center gap-4 text-xs text-gray-500">
                        <span className="flex items-center gap-1">
                          <CalendarIcon className="w-4 h-4" />
                          {new Date(log.timestamp).toLocaleString()}
                        </span>
                        <span>User: {log.user}</span>
                      </div>
                    </div>
                    <button
                      onClick={() => alert(`View log details: ${log.id}`)}
                      className="text-purple-600 hover:text-purple-800 text-sm font-medium"
                    >
                      View Details
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {['all', 'auth', 'transaction', 'loan', 'security'].map((type) => (
            <div key={type} className="bg-white rounded-xl shadow-sm p-4">
              <p className="text-xs text-gray-500 mb-1 uppercase">{type === 'all' ? 'Total' : type}</p>
              <p className="text-xl font-bold text-gray-800">
                {type === 'all' ? logs.length : logs.filter(l => l.type === type).length}
              </p>
            </div>
          ))}
        </div>
      </div>
    </MainLayout>
  );
}
