'use client';

import { useState, useEffect } from 'react';
import MainLayout from '@/components/Layout/MainLayout';
import CreditCard from '@/components/Cards/CreditCard';
import api from '@/lib/api';

export default function Transactions() {
  const [activeTab, setActiveTab] = useState<'all' | 'income' | 'expense'>('all');
  const [transactions, setTransactions] = useState<any[]>([]);
  const [cards, setCards] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({
    description: '',
    amount: '',
    type: 'EXPENSE',
    date: '',
    category: ''
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [txnRes, cardRes] = await Promise.all([
        api.get('/transactions/'),
        api.get('/bank-accounts/')
      ]);
      const txns = Array.isArray(txnRes.data)
        ? txnRes.data
        : (txnRes.data?.results ? txnRes.data.results : []);
      setTransactions(txns);
      setCards(Array.isArray(cardRes.data) ? cardRes.data : []);
    } catch (err) {
      console.error('Error fetching data:', err);
      setTransactions([]);
      setCards([]);
    } finally {
      setLoading(false);
    }
  };

  const filteredTransactions = transactions.filter(t => {
    if (activeTab === 'all') return true;
    if (activeTab === 'income') return (t.transaction_type || t.type) === 'INCOME';
    return (t.transaction_type || t.type) === 'EXPENSE';
  });

  return (
    <MainLayout title="Transactions">
      <div className="space-y-6">
        {/* Add Transaction */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Add Transaction</h2>
          {error && <div className="mb-3 text-sm text-red-700 bg-red-50 border border-red-200 rounded p-2">{error}</div>}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
            <input
              className="border rounded px-3 py-2"
              placeholder="Description"
              value={form.description}
              onChange={e => setForm({ ...form, description: e.target.value })}
            />
            <input
              type="number"
              step="0.01"
              className="border rounded px-3 py-2"
              placeholder="Amount"
              value={form.amount}
              onChange={e => setForm({ ...form, amount: e.target.value })}
            />
            <select
              className="border rounded px-3 py-2"
              value={form.type}
              onChange={e => setForm({ ...form, type: e.target.value })}
            >
              <option value="INCOME">Income</option>
              <option value="EXPENSE">Expense</option>
            </select>
            <input
              type="date"
              className="border rounded px-3 py-2"
              value={form.date}
              onChange={e => setForm({ ...form, date: e.target.value })}
            />
          </div>
          <div className="mt-3">
            <button
              disabled={saving}
              onClick={async () => {
                setSaving(true);
                setError(null);
                try {
                  const body: any = {
                    description: form.description || null,
                    amount: parseFloat(form.amount),
                    type: form.type,
                    date: form.date || new Date().toISOString().slice(0,10),
                    source: 'MANUAL'
                  };
                  const res = await api.post('/transactions/', body);
                  const t = res.data;
                  const uiItem = {
                    id: t.id,
                    description: t.description || form.description,
                    category_name: t.category?.name || 'Uncategorized',
                    transaction_type: t.type,
                    date: t.date,
                    amount: t.amount
                  };
                  setTransactions(prev => [uiItem, ...prev]);
                  setForm({ description: '', amount: '', type: 'EXPENSE', date: '', category: '' });
                } catch (err: any) {
                  setError(err?.response?.data?.detail || err?.response?.data?.error || 'Failed to add transaction');
                } finally {
                  setSaving(false);
                }
              }}
              className="px-4 py-2 bg-blue-600 text-white rounded"
            >
              {saving ? 'Saving...' : 'Add Transaction'}
            </button>
          </div>
        </div>

        {/* Primary Card Section */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-800">Your Cards</h2>
            <button
              onClick={() => window.location.href = '/cards'}
              className="text-sm text-blue-600 hover:underline"
            >
              See All
            </button>
          </div>
          {cards.length === 0 ? (
            <div className="text-center py-8 text-gray-400">
              <div className="text-4xl mb-2">💳</div>
              <p>No cards added yet</p>
              <p className="text-sm mt-1">Add a card from the Cards page</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {cards.slice(0, 2).map((card, idx) => (
                <CreditCard
                  key={card.id || idx}
                  balance="E£ ****.**"
                  cardHolder={card.institution_name || 'Card Holder'}
                  validThru="**/**"
                  cardNumber={`**** **** **** ${card.token?.slice(-4) || '****'}`}
                />
              ))}
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 gap-6">
          {/* Recent Transactions */}
          <div className="bg-white rounded-xl shadow-sm p-6">
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

            {loading ? (
              <div className="text-center py-8 text-gray-400">Loading transactions...</div>
            ) : filteredTransactions.length === 0 ? (
              <div className="text-center py-8 text-gray-400">
                <div className="text-4xl mb-2">📊</div>
                <p>No {activeTab !== 'all' ? activeTab : ''} transactions yet</p>
                <p className="text-sm mt-1">Start by adding your transactions</p>
              </div>
            ) : (
              <>
                {/* Transactions Table */}
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-gray-200">
                        <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Description</th>
                        <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Category</th>
                        <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Type</th>
                        <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Date</th>
                        <th className="text-left py-3 px-4 text-sm font-semibold text-gray-600">Amount</th>
                      </tr>
                    </thead>
                    <tbody>
                      {filteredTransactions.map((transaction) => (
                        <tr key={transaction.id} className="border-b border-gray-100 hover:bg-gray-50">
                          <td className="py-3 px-4">
                            <div className="flex items-center gap-2">
                              <span className="text-xl">
                                {(transaction.transaction_type || transaction.type) === 'INCOME' ? '💰' : '💸'}
                              </span>
                              <span className="font-medium text-gray-800">
                                {transaction.description || 'Transaction'}
                              </span>
                              {(transaction.transaction_type || transaction.type) === 'INCOME' ? (
                                <span className="text-green-500">↑</span>
                              ) : (
                                <span className="text-red-500">↓</span>
                              )}
                            </div>
                          </td>
                          <td className="py-3 px-4 text-sm text-gray-600">
                            {transaction.category_name || 'Uncategorized'}
                          </td>
                          <td className="py-3 px-4 text-sm text-gray-600">
                            {transaction.transaction_type || transaction.type || 'N/A'}
                          </td>
                          <td className="py-3 px-4 text-sm text-gray-600">
                            {new Date(transaction.date || transaction.created_at).toLocaleDateString()}
                          </td>
                          <td className={`py-3 px-4 font-semibold ${
                            (transaction.transaction_type || transaction.type) === 'INCOME' ? 'text-green-600' : 'text-red-600'
                          }`}>
                            {(transaction.transaction_type || transaction.type) === 'INCOME' ? '+' : '-'}E£{Math.abs(transaction.amount).toLocaleString()}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

