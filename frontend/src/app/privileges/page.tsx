'use client';

import { useEffect, useState } from 'react';
import MainLayout from '@/components/Layout/MainLayout';
import api from '@/lib/api';
import { ShieldCheckIcon, LockClosedIcon, EyeIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline';

export default function Privileges() {
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await api.get('/auth/profile/');
        setUser(res.data.user || null);
      } catch (err) {
        console.error('Error fetching profile:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  const privileges = [
    {
      category: 'Financial Management',
      permissions: [
        { name: 'View Transactions', icon: EyeIcon, granted: true, description: 'View all your transaction history' },
        { name: 'Create Transactions', icon: PencilIcon, granted: true, description: 'Add new income and expense transactions' },
        { name: 'Edit Transactions', icon: PencilIcon, granted: true, description: 'Modify existing transactions' },
        { name: 'Delete Transactions', icon: TrashIcon, granted: true, description: 'Remove transactions from your records' },
      ]
    },
    {
      category: 'Budget & Goals',
      permissions: [
        { name: 'Create Budgets', icon: PencilIcon, granted: true, description: 'Set up monthly budget limits' },
        { name: 'View Budget Reports', icon: EyeIcon, granted: true, description: 'Access detailed budget analytics' },
        { name: 'Manage Goals', icon: PencilIcon, granted: true, description: 'Create and track financial goals' },
        { name: 'Goal Analytics', icon: EyeIcon, granted: true, description: 'View goal progress and insights' },
      ]
    },
    {
      category: 'Accounts & Cards',
      permissions: [
        { name: 'Link Bank Accounts', icon: PencilIcon, granted: true, description: 'Connect external bank accounts' },
        { name: 'Manage Cards', icon: PencilIcon, granted: true, description: 'Add and manage credit/debit cards' },
        { name: 'View Account Balance', icon: EyeIcon, granted: true, description: 'Check real-time account balances' },
        { name: 'Transfer Funds', icon: PencilIcon, granted: true, description: 'Transfer money between accounts' },
      ]
    },
    {
      category: 'Loans & Investments',
      permissions: [
        { name: 'Apply for Loans', icon: PencilIcon, granted: true, description: 'Submit loan applications' },
        { name: 'View Loan Details', icon: EyeIcon, granted: true, description: 'Access loan terms and payments' },
        { name: 'Manage Investments', icon: PencilIcon, granted: true, description: 'Track investment portfolio' },
        { name: 'Investment Reports', icon: EyeIcon, granted: true, description: 'View investment performance' },
      ]
    },
    {
      category: 'Security & Privacy',
      permissions: [
        { name: 'Enable 2FA', icon: ShieldCheckIcon, granted: true, description: 'Two-factor authentication access' },
        { name: 'Change Password', icon: LockClosedIcon, granted: true, description: 'Update account password' },
        { name: 'Session Management', icon: EyeIcon, granted: true, description: 'View and control active sessions' },
        { name: 'Data Export', icon: EyeIcon, granted: true, description: 'Export your personal financial data' },
      ]
    },
    {
      category: 'AI & Automation',
      permissions: [
        { name: 'AI Chatbot', icon: EyeIcon, granted: true, description: 'Access AI financial assistant' },
        { name: 'Smart Alerts', icon: EyeIcon, granted: true, description: 'Receive AI-powered notifications' },
        { name: 'Spending Insights', icon: EyeIcon, granted: true, description: 'Get personalized spending analysis' },
        { name: 'Budget Recommendations', icon: EyeIcon, granted: true, description: 'Receive budget optimization tips' },
      ]
    },
  ];

  if (loading) {
    return (
      <MainLayout title="My Privileges">
        <div className="bg-white rounded-xl shadow-sm p-6 text-center">
          <p className="text-gray-600">Loading...</p>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout title="My Privileges">
      <div className="space-y-6">
        {/* User Info Card */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-xl shadow-sm p-6 text-white">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center">
              <ShieldCheckIcon className="w-8 h-8" />
            </div>
            <div>
              <h2 className="text-2xl font-bold">
                {user?.first_name || user?.email || 'User'}
              </h2>
              <p className="text-blue-100">Account Type: Standard User</p>
              <p className="text-sm text-blue-200 mt-1">Member since {new Date().getFullYear()}</p>
            </div>
          </div>
        </div>

        {/* Privileges List */}
        {privileges.map((section, idx) => (
          <div key={idx} className="bg-white rounded-xl shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <ShieldCheckIcon className="w-5 h-5 text-blue-600" />
              {section.category}
            </h3>
            <div className="space-y-3">
              {section.permissions.map((perm, pidx) => {
                const Icon = perm.icon;
                return (
                  <div 
                    key={pidx} 
                    className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                        perm.granted ? 'bg-green-100' : 'bg-gray-200'
                      }`}>
                        <Icon className={`w-5 h-5 ${
                          perm.granted ? 'text-green-600' : 'text-gray-400'
                        }`} />
                      </div>
                      <div>
                        <p className="font-medium text-gray-800">{perm.name}</p>
                        <p className="text-sm text-gray-500">{perm.description}</p>
                      </div>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                      perm.granted 
                        ? 'bg-green-100 text-green-700' 
                        : 'bg-gray-200 text-gray-600'
                    }`}>
                      {perm.granted ? 'Granted' : 'Restricted'}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        ))}

        {/* Additional Info */}
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
          <div className="flex items-start gap-3">
            <ShieldCheckIcon className="w-6 h-6 text-blue-600 flex-shrink-0 mt-1" />
            <div>
              <h4 className="font-semibold text-blue-900 mb-2">About Your Privileges</h4>
              <p className="text-sm text-blue-800 leading-relaxed">
                These privileges define what actions you can perform within the Funder platform. 
                As a standard user, you have full access to manage your personal finances, budgets, 
                and goals. If you need additional permissions or have questions about your account 
                privileges, please contact our support team.
              </p>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

