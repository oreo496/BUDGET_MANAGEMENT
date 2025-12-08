'use client';

import { useState } from 'react';
import MainLayout from '@/components/Layout/MainLayout';
import CreditCard from '@/components/Cards/CreditCard';
import BarChart from '@/components/Charts/BarChart';

export default function Transactions() {
  const [activeTab, setActiveTab] = useState<'all' | 'income' | 'expense'>('all');

  const monthlyExpense = [
    { label: 'Aug', value: 8000 },
    { label: 'Sep', value: 9500 },
    { label: 'Oct', value: 11000 },
    { label: 'Nov', value: 10000 },
    { label: 'Dec', value: 12500, color: '#14b8a6' },
    { label: 'Jan', value: 10500 },
  ];

  const transactions = [
    {
      id: 1,
      description: 'Spotify Subscription',
      transactionId: '#12548796',
      type: 'Shopping',
      card: '1234****',
      date: '28 Jan, 12.30 AM',
      amount: -2500,
      icon: '🎵',
      isIncome: false,
    },
    {
      id: 2,
      description: 'Freepik Sales',
      transactionId: '#12548796',
      type: 'Transfer',
      card: '1234****',
      date: '25 Jan, 10.40 PM',
      amount: 750,
      icon: '💰',
      isIncome: true,
    },
    {
      id: 3,
      description: 'Mobile Service',
      transactionId: '#12548796',
      type: 'Service',
      card: '1234****',
      date: '20 Jan, 10.40 PM',
      amount: -150,
      icon: '📱',
      isIncome: false,
    },
    {
      id: 4,
      description: 'Wilson',
      transactionId: '#12548796',
      type: 'Transfer',
      card: '1234****',
      date: '15 Jan, 03.29 PM',
      amount: -1050,
      icon: '👤',
      isIncome: false,
    },
    {
      id: 5,
      description: 'Emily',
      transactionId: '#12548796',
      type: 'Transfer',
      card: '1234****',
      date: '14 Jan, 10.40 PM',
      amount: 840,
      icon: '👤',
      isIncome: true,
    },
  ];

  const filteredTransactions = transactions.filter(t => {
    if (activeTab === 'all') return true;
    if (activeTab === 'income') return t.isIncome;
    return !t.isIncome;
  });

  return (
    <MainLayout title="Transactions">
      <div className="space-y-6">
        {/* Primary Card Section */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-800">Primary Card</h2>
            <button
              onClick={() => window.location.href = '/cards'}
              className="text-sm text-blue-600 hover:underline"
            >
              See All
            </button>
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

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* My Expense Chart */}
          <div className="lg:col-span-1 bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">My Expense</h2>
            <BarChart data={monthlyExpense} height={250} showValues />
          </div>

          {/* Recent Transactions */}
          <div className="lg:col-span-2 bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-800">Recent Transactions</h2>
            </div>

            {/* Tabs */}
            <div className="flex gap-2 mb-4 border-b border-gray-200">
              <button
                onClick={() => setActiveTab('all')}
                className={`px-4 py-2 font-medium transition-colors ${
                  activeTab === 'all'
                    ? 'text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                All Transactions
              </button>
              <button
                onClick={() => setActiveTab('income')}
                className={`px-4 py-2 font-medium transition-colors ${
                  activeTab === 'income'
                    ? 'text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                Income
              </button>
              <button
                onClick={() => setActiveTab('expense')}
                className={`px-4 py-2 font-medium transition-colors ${
                  activeTab === 'expense'
                    ? 'text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                Expense
              </button>
            </div>

            {/* Transactions Table */}
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Description</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Transaction ID</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Type</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Card</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Date</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Amount</th>
                    <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Receipt</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredTransactions.map((transaction) => (
                    <tr key={transaction.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-3 px-4">
                        <div className="flex items-center gap-2">
                          <span className="text-xl">{transaction.icon}</span>
                          <span className="font-medium text-gray-800">{transaction.description}</span>
                          {transaction.isIncome ? (
                            <span className="text-green-500">↑</span>
                          ) : (
                            <span className="text-red-500">↓</span>
                          )}
                        </div>
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-600">{transaction.transactionId}</td>
                      <td className="py-3 px-4 text-sm text-gray-600">{transaction.type}</td>
                      <td className="py-3 px-4 text-sm text-gray-600">{transaction.card}</td>
                      <td className="py-3 px-4 text-sm text-gray-600">{transaction.date}</td>
                      <td className={`py-3 px-4 font-semibold ${
                        transaction.amount > 0 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {transaction.amount > 0 ? '+' : ''}E£{Math.abs(transaction.amount).toLocaleString()}
                      </td>
                      <td className="py-3 px-4">
                        <button
                          onClick={() => {
                            alert(`Downloading receipt for ${transaction.description}...`);
                            // In real app, this would download the receipt PDF
                          }}
                          className="text-blue-600 hover:underline text-sm"
                        >
                          Download
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            <div className="flex items-center justify-end gap-2 mt-4">
              <button
                onClick={() => alert('Previous page')}
                className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
              >
                Previous
              </button>
              <button
                onClick={() => alert('Page 1')}
                className="px-3 py-1 text-sm bg-blue-600 text-white rounded"
              >
                1
              </button>
              <button
                onClick={() => alert('Page 2')}
                className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
              >
                2
              </button>
              <button
                onClick={() => alert('Page 3')}
                className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
              >
                3
              </button>
              <button
                onClick={() => alert('Page 4')}
                className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
              >
                4
              </button>
              <button
                onClick={() => alert('Next page')}
                className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

