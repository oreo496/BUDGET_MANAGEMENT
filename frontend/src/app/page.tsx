'use client';

import { useState } from 'react';
import MainLayout from '@/components/Layout/MainLayout';
import CreditCard from '@/components/Cards/CreditCard';
import BarChart from '@/components/Charts/BarChart';
import PieChart from '@/components/Charts/PieChart';
import LineChart from '@/components/Charts/LineChart';

export default function Dashboard() {
  const [transferAmount, setTransferAmount] = useState('E£525.50');
  const [selectedRecipient, setSelectedRecipient] = useState<string | null>(null);
  const weeklyActivity = [
    { label: 'Sat', value: 450, color: '#3b82f6' },
    { label: 'Sun', value: 320, color: '#1e40af' },
    { label: 'Mon', value: 280, color: '#3b82f6' },
    { label: 'Tue', value: 380, color: '#1e40af' },
    { label: 'Wed', value: 250, color: '#3b82f6' },
    { label: 'Thu', value: 400, color: '#1e40af' },
    { label: 'Fri', value: 350, color: '#3b82f6' },
  ];

  const expenseStats = [
    { label: 'Entertainment', value: 30, color: '#1e40af' },
    { label: 'Bill Expense', value: 15, color: '#f97316' },
    { label: 'Investment', value: 20, color: '#ec4899' },
    { label: 'Others', value: 35, color: '#9ca3af' },
  ];

  const balanceHistory = [
    { label: 'Jul', value: 200 },
    { label: 'Aug', value: 350 },
    { label: 'Sep', value: 280 },
    { label: 'Oct', value: 600 },
    { label: 'Nov', value: 450 },
    { label: 'Dec', value: 550 },
    { label: 'Jan', value: 700 },
  ];

  return (
    <MainLayout title="Overview">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Primary Card */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-800">Primary Card</h2>
            <a
              href="/cards"
              className="text-sm text-blue-600 hover:underline"
            >
              See All
            </a>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <CreditCard
              balance="E£ 273,907.37"
              cardHolder="Mohamed Elhosieny"
              validThru="07/28"
              cardNumber="3778 **** **** 1234"
            />
            <CreditCard
              balance="E£ 273,907.37"
              cardNumber="3778 **** **** 1234"
              showCVV
            />
          </div>
        </div>

        {/* Recent Transaction */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-800">Recent Transaction</h2>
            <button
              onClick={() => window.location.href = '/cards'}
              className="text-sm text-blue-600 hover:underline"
            >
              See All
            </button>
          </div>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                  <span className="text-blue-600 text-xl">💳</span>
                </div>
                <div>
                  <div className="font-medium text-gray-800">Deposit from my Card</div>
                  <div className="text-sm text-gray-500">28 January 2021</div>
                </div>
              </div>
              <div className="text-red-600 font-semibold">-E£850</div>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                  <span className="text-green-600 text-xl">P</span>
                </div>
                <div>
                  <div className="font-medium text-gray-800">Deposit Paypal</div>
                  <div className="text-sm text-gray-500">25 January 2021</div>
                </div>
              </div>
              <div className="text-green-600 font-semibold">+E£2,500</div>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
                  <span className="text-purple-600 text-xl">👤</span>
                </div>
                <div>
                  <div className="font-medium text-gray-800">Jemi Wilson</div>
                  <div className="text-sm text-gray-500">21 January 2021</div>
                </div>
              </div>
              <div className="text-green-600 font-semibold">+E£5,400</div>
            </div>
          </div>
        </div>

        {/* Weekly Activity */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Weekly Activity</h2>
          <div className="flex items-center gap-4 mb-4">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-blue-400 rounded-full"></div>
              <span className="text-sm text-gray-600">Deposit</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-blue-800 rounded-full"></div>
              <span className="text-sm text-gray-600">Withdraw</span>
            </div>
          </div>
          <BarChart data={weeklyActivity} height={200} />
        </div>

        {/* Expense Statistics */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Expense Statistics</h2>
          <PieChart data={expenseStats} size={180} />
        </div>

        {/* Quick Transfer */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Quick Transfer</h2>
          <div className="flex items-center gap-4 mb-6">
            <button
              onClick={() => setSelectedRecipient('livia')}
              className={`flex flex-col items-center transition-opacity ${
                selectedRecipient === 'livia' ? 'opacity-100' : 'opacity-60 hover:opacity-80'
              }`}
            >
              <div className={`w-12 h-12 rounded-full flex items-center justify-center mb-2 ${
                selectedRecipient === 'livia' ? 'bg-blue-600' : 'bg-blue-100'
              }`}>
                <span className={`font-semibold ${
                  selectedRecipient === 'livia' ? 'text-white' : 'text-blue-600'
                }`}>LB</span>
              </div>
              <span className="text-xs text-gray-600">Livia Bator</span>
              <span className="text-xs text-gray-500">CEO</span>
            </button>
            <button
              onClick={() => setSelectedRecipient('randy')}
              className={`flex flex-col items-center transition-opacity ${
                selectedRecipient === 'randy' ? 'opacity-100' : 'opacity-60 hover:opacity-80'
              }`}
            >
              <div className={`w-12 h-12 rounded-full flex items-center justify-center mb-2 ${
                selectedRecipient === 'randy' ? 'bg-orange-600' : 'bg-orange-100'
              }`}>
                <span className={`font-semibold ${
                  selectedRecipient === 'randy' ? 'text-white' : 'text-orange-600'
                }`}>RP</span>
              </div>
              <span className="text-xs text-gray-600">Randy Press</span>
              <span className="text-xs text-gray-500">Director</span>
            </button>
            <button
              onClick={() => setSelectedRecipient('workman')}
              className={`flex flex-col items-center transition-opacity ${
                selectedRecipient === 'workman' ? 'opacity-100' : 'opacity-60 hover:opacity-80'
              }`}
            >
              <div className={`w-12 h-12 rounded-full flex items-center justify-center mb-2 ${
                selectedRecipient === 'workman' ? 'bg-pink-600' : 'bg-pink-100'
              }`}>
                <span className={`font-semibold ${
                  selectedRecipient === 'workman' ? 'text-white' : 'text-pink-600'
                }`}>W</span>
              </div>
              <span className="text-xs text-gray-600">Workman</span>
              <span className="text-xs text-gray-500">Designer</span>
            </button>
            <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center">
              <span className="text-gray-600">→</span>
            </div>
          </div>
          <div className="space-y-3">
            <input
              type="text"
              placeholder="Write Amount"
              value={transferAmount}
              onChange={(e) => setTransferAmount(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={() => {
                if (!selectedRecipient) {
                  alert('Please select a recipient');
                  return;
                }
                const amount = transferAmount.replace(/[^0-9.]/g, '');
                if (!amount || parseFloat(amount) <= 0) {
                  alert('Please enter a valid amount');
                  return;
                }
                alert(`Transfer of ${transferAmount} to ${selectedRecipient} initiated!`);
                setTransferAmount('E£0.00');
                setSelectedRecipient(null);
              }}
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
            >
              Send
            </button>
          </div>
        </div>

        {/* Balance History */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Balance History</h2>
          <LineChart data={balanceHistory} height={200} color="#3b82f6" />
        </div>
      </div>
    </MainLayout>
  );
}
