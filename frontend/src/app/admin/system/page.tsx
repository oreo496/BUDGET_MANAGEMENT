'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import AdminLayout from '@/components/Layout/AdminLayout';
import api from '@/lib/api';
import { 
  ServerIcon,
  CircleStackIcon,
  UsersIcon,
  BanknotesIcon,
  CreditCardIcon,
  ChartBarIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';

export default function SystemManagement() {
  const router = useRouter();
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const adminToken = localStorage.getItem('adminToken');
    if (!adminToken) {
      router.push('/admin/login');
      return;
    }
    fetchStats();
  }, [router]);

  const fetchStats = async () => {
    try {
      console.log('Fetching system stats from admin API...');
      const res = await api.get('/admin/system/stats/');
      console.log('Stats fetched:', res.data);
      setStats(res.data);
    } catch (err: any) {
      console.error('Error fetching system stats:', err);
      console.error('Error response:', err?.response?.data);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <AdminLayout title="System Management">
        <div className="flex items-center justify-center h-64">
          <div className="text-gray-600">Loading system information...</div>
        </div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout title="System Management">
      <div className="space-y-6">
        {/* Header */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <ServerIcon className="w-6 h-6 text-blue-600" />
            System Management
          </h2>
          <p className="text-gray-600 mt-2">Monitor and manage system resources</p>
        </div>

        {/* System Status */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <CheckCircleIcon className="w-5 h-5 text-green-600" />
            System Status
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg">
              <div className="flex items-center gap-3">
                <CircleStackIcon className="w-8 h-8 text-green-600" />
                <div>
                  <p className="text-sm text-gray-600">Database</p>
                  <p className="text-lg font-semibold text-gray-800">{stats?.system?.database_status || 'Connected'}</p>
                </div>
              </div>
              <span className="px-3 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">
                Online
              </span>
            </div>
            
            <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
              <div className="flex items-center gap-3">
                <ServerIcon className="w-8 h-8 text-blue-600" />
                <div>
                  <p className="text-sm text-gray-600">API Version</p>
                  <p className="text-lg font-semibold text-gray-800">{stats?.system?.api_version || '1.0.0'}</p>
                </div>
              </div>
              <span className="px-3 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">
                Active
              </span>
            </div>
          </div>
        </div>

        {/* Users Statistics */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <UsersIcon className="w-5 h-5 text-blue-600" />
            User Statistics
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Total Users</p>
              <p className="text-3xl font-bold text-gray-800">{stats?.users?.total || 0}</p>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Active Users</p>
              <p className="text-3xl font-bold text-green-600">{stats?.users?.active || 0}</p>
            </div>
            <div className="p-4 bg-red-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Inactive Users</p>
              <p className="text-3xl font-bold text-red-600">{stats?.users?.inactive || 0}</p>
            </div>
          </div>
        </div>

        {/* Loans Statistics */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <BanknotesIcon className="w-5 h-5 text-purple-600" />
            Loan Statistics
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Total Loans</p>
              <p className="text-3xl font-bold text-gray-800">{stats?.loans?.total || 0}</p>
            </div>
            <div className="p-4 bg-yellow-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Pending</p>
              <p className="text-3xl font-bold text-yellow-600">{stats?.loans?.pending || 0}</p>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Approved</p>
              <p className="text-3xl font-bold text-green-600">{stats?.loans?.approved || 0}</p>
            </div>
            <div className="p-4 bg-red-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Rejected</p>
              <p className="text-3xl font-bold text-red-600">{stats?.loans?.rejected || 0}</p>
            </div>
          </div>
        </div>

        {/* Transactions & Accounts */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <ChartBarIcon className="w-5 h-5 text-teal-600" />
              Transactions
            </h3>
            <div className="p-4 bg-teal-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Total Transactions</p>
              <p className="text-4xl font-bold text-teal-600">{stats?.transactions?.total || 0}</p>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <CreditCardIcon className="w-5 h-5 text-indigo-600" />
              Bank Accounts
            </h3>
            <div className="p-4 bg-indigo-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">Total Accounts</p>
              <p className="text-4xl font-bold text-indigo-600">{stats?.accounts?.total || 0}</p>
            </div>
          </div>
        </div>

        {/* System Actions */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">System Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <button
              onClick={() => {
                fetchStats();
                alert('System statistics refreshed');
              }}
              className="p-4 border-2 border-blue-200 rounded-lg hover:bg-blue-50 transition-colors"
            >
              <div className="text-center">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
                  <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                </div>
                <p className="font-medium text-gray-800">Refresh Stats</p>
                <p className="text-sm text-gray-600 mt-1">Update system statistics</p>
              </div>
            </button>

            <button
              onClick={() => window.location.href = '/admin/users'}
              className="p-4 border-2 border-green-200 rounded-lg hover:bg-green-50 transition-colors"
            >
              <div className="text-center">
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
                  <UsersIcon className="w-6 h-6 text-green-600" />
                </div>
                <p className="font-medium text-gray-800">Manage Users</p>
                <p className="text-sm text-gray-600 mt-1">User administration</p>
              </div>
            </button>
          </div>
        </div>
      </div>
    </AdminLayout>
  );
}
