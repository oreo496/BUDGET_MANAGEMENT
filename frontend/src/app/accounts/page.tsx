'use client';

import { useState, useEffect } from 'react';
import MainLayout from '@/components/Layout/MainLayout';
import CreditCard from '@/components/Cards/CreditCard';
import BarChart from '@/components/Charts/BarChart';

export default function Accounts() {
  const [balance, setBalance] = useState(0);
  const [income, setIncome] = useState(0);
  const [expense, setExpense] = useState(0);
  const [savings, setSavings] = useState(0);
  const [recentTransactions, setRecentTransactions] = useState<any[]>([]);
  const [cards, setCards] = useState<any[]>([]);
  const [debitCreditData, setDebitCreditData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAccountData();
  }, []);

  const fetchAccountData = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      setLoading(false);
      return;
    }

    try {
      const [txnRes, cardsRes] = await Promise.all([
        fetch('http://localhost:8000/api/transactions/', {
          headers: { Authorization: `Bearer ${token}` },
        }).catch(() => null),
        fetch('http://localhost:8000/api/bank-accounts/', {
          headers: { Authorization: `Bearer ${token}` },
        }).catch(() => null),
      ]);

      if (txnRes?.ok) {
        const txnData = await txnRes.json();
        const transactions = Array.isArray(txnData) ? txnData : txnData.results || [];
        
        // Calculate totals
        let totalIncome = 0;
        let totalExpense = 0;
        transactions.forEach((txn: any) => {
          if (txn.type === 'INCOME') {
            totalIncome += parseFloat(txn.amount || 0);
          } else {
            totalExpense += parseFloat(txn.amount || 0);
          }
        });

        setIncome(totalIncome);
        setExpense(totalExpense);
        setBalance(totalIncome - totalExpense);
        setSavings(totalIncome - totalExpense);
        setRecentTransactions(transactions.slice(0, 3));
      }

      if (cardsRes?.ok) {
        const cardsData = await cardsRes.json();
        const cardsArray = Array.isArray(cardsData) ? cardsData : [];
        setCards(cardsArray);
      }
    } catch (error) {
      console.error('Error fetching account data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <MainLayout title="Accounts">
      <div className="space-y-6">
        {/* Financial Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">💰</span>
              </div>
              <div>
                <div className="text-sm text-gray-500">My Balance</div>
                <div className="text-2xl font-bold text-gray-800">E£{balance.toFixed(2)}</div>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">💵</span>
              </div>
              <div>
                <div className="text-sm text-gray-500">Income</div>
                <div className="text-2xl font-bold text-gray-800">E£{income.toFixed(2)}</div>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">🏢</span>
              </div>
              <div>
                <div className="text-sm text-gray-500">Expense</div>
                <div className="text-2xl font-bold text-gray-800">E£{expense.toFixed(2)}</div>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">🐷</span>
              </div>
              <div>
                <div className="text-sm text-gray-500">Total Saving</div>
                <div className="text-2xl font-bold text-gray-800">E£{savings.toFixed(2)}</div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Last Transaction */}
          <div className="lg:col-span-1 bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Recent Transactions</h2>
            {recentTransactions.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <p>No transactions yet</p>
              </div>
            ) : (
              <div className="space-y-4">
                {recentTransactions.map((txn: any) => (
                  <div key={txn.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                        txn.type === 'INCOME' ? 'bg-green-100' : 'bg-red-100'
                      }`}>
                        <span className={txn.type === 'INCOME' ? 'text-green-600 text-xl' : 'text-red-600 text-xl'}>
                          {txn.type === 'INCOME' ? '💵' : '💳'}
                        </span>
                      </div>
                      <div>
                        <div className="font-medium text-gray-800">{txn.description || 'Transaction'}</div>
                        <div className="text-xs text-gray-500">
                          {new Date(txn.date || txn.created_at).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className={`font-semibold ${txn.type === 'INCOME' ? 'text-green-600' : 'text-red-600'}`}>
                        {txn.type === 'INCOME' ? '+' : '-'}E£{Math.abs(txn.amount).toFixed(2)}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* My Card */}
          <div className="lg:col-span-1 bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-800">My Card</h2>
              <a href="/cards" className="text-sm text-blue-600 hover:underline">+Add Card</a>
            </div>
            {cards.length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                <p>No cards added yet</p>
              </div>
            ) : (
              <CreditCard
                balance={`E£ ${cards[0]?.balance || '0.00'}`}
                cardHolder={cards[0]?.institution_name || 'Card'}
                cardNumber={`**** **** **** ${cards[0]?.token?.slice(-4) || '****'}`}
              />
            )}
          </div>

          {/* Debit & Credit Overview */}
          <div className="lg:col-span-1 bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Debit & Credit Overview</h2>
            {debitCreditData.length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                <p>No data available yet</p>
              </div>
            ) : (
              <>
                <p className="text-sm text-gray-600 mb-4">
                  E£{expense.toFixed(2)} Debited & E£{income.toFixed(2)} Credited
                </p>
                <div className="flex items-center gap-4 mb-4">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-blue-600 rounded"></div>
                    <span className="text-sm text-gray-600">Debit</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-orange-500 rounded"></div>
                    <span className="text-sm text-gray-600">Credit</span>
                  </div>
                </div>
                <BarChart data={debitCreditData} height={200} />
              </>
            )}
          </div>
        </div>

        {/* Invoices Sent - Removed fake data */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Invoices</h2>
          <div className="text-center py-8 text-gray-500">
            <p>Invoice feature coming soon!</p>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

