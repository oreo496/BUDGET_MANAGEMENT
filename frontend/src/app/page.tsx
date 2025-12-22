'use client';

import { useState, useEffect } from 'react';
import MainLayout from '@/components/Layout/MainLayout';
import CreditCard from '@/components/Cards/CreditCard';
import BarChart from '@/components/Charts/BarChart';
import PieChart from '@/components/Charts/PieChart';
import LineChart from '@/components/Charts/LineChart';
import {
  SparklesIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ChartBarIcon,
  CurrencyDollarIcon,
  ArrowTrendingUpIcon,
  ShieldExclamationIcon,
} from '@heroicons/react/24/outline';

export default function Dashboard() {
  const [transferAmount, setTransferAmount] = useState('E£525.50');
  const [selectedRecipient, setSelectedRecipient] = useState<string | null>(null);
  const [transactionPrediction, setTransactionPrediction] = useState<any>(null);
  const [budgetRisk, setBudgetRisk] = useState<any>(null);
  const [goalSuccess, setGoalSuccess] = useState<any>(null);
  const [fraudDetection, setFraudDetection] = useState<any>(null);
  const [loadingAI, setLoadingAI] = useState(true);
  const [weeklyActivity, setWeeklyActivity] = useState<any[]>([]);
  const [expenseStats, setExpenseStats] = useState<any[]>([]);
  const [balanceHistory, setBalanceHistory] = useState<any[]>([]);
  const [recentTransactions, setRecentTransactions] = useState<any[]>([]);
  const [userCards, setUserCards] = useState<any[]>([]);

  useEffect(() => {
    const fetchAllAIInsights = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        setLoadingAI(false);
        return;
      }

      setLoadingAI(true);

      // Fetch real transactions, cards, and user data
      try {
        const [txnResponse, cardsResponse] = await Promise.all([
          fetch('http://localhost:8000/api/transactions/', {
            headers: { Authorization: `Bearer ${token}` },
          }).catch(() => null),
          fetch('http://localhost:8000/api/bank-accounts/', {
            headers: { Authorization: `Bearer ${token}` },
          }).catch(() => null),
        ]);

        if (txnResponse?.ok) {
          const txnData = await txnResponse.json();
          const transactions = Array.isArray(txnData) ? txnData : txnData.results || [];
          setRecentTransactions(transactions.slice(0, 3));
          
          // Only fetch AI predictions if user has transaction history
          if (transactions.length === 0) {
            console.log('No transactions found - skipping AI predictions');
            setLoadingAI(false);
            return;
          }
        } else {
          console.log('Failed to fetch transactions - skipping AI predictions');
          setLoadingAI(false);
          return;
        }

        if (cardsResponse?.ok) {
          const cardsData = await cardsResponse.json();
          const cards = Array.isArray(cardsData) ? cardsData : [];
          setUserCards(cards.slice(0, 2));
        }
      } catch (error) {
        console.error('Error fetching real data:', error);
        setLoadingAI(false);
        return;
      }
      
      // Fetch all 4 AI predictions in parallel
      try {
        const [txnRes, budgetRes, goalRes, fraudRes] = await Promise.all([
          fetch('http://localhost:8000/api/ai-alerts/predict/transaction/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              amount: 250.75,
              merchant: 'Amazon',
              date: new Date().toISOString().split('T')[0],
            }),
          }).catch(() => null),
          
          fetch('http://localhost:8000/api/ai-alerts/predict/budget-risk/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              budget_id: 1,
              current_spending: 850,
              budget_limit: 1000,
            }),
          }).catch(() => null),
          
          fetch('http://localhost:8000/api/ai-alerts/predict/goal-success/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              goal_id: 1,
              target_amount: 5000,
              current_amount: 3500,
              deadline: '2026-06-30',
            }),
          }).catch(() => null),
          
          fetch('http://localhost:8000/api/ai-alerts/predict/flagged/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              amount: 50.00,
              merchant: 'Local Store',
              location: 'Same City',
              time: '2:00 PM',
            }),
          }).catch(() => null),
        ]);

        if (txnRes?.ok) setTransactionPrediction(await txnRes.json());
        if (budgetRes?.ok) setBudgetRisk(await budgetRes.json());
        if (goalRes?.ok) setGoalSuccess(await goalRes.json());
        if (fraudRes?.ok) setFraudDetection(await fraudRes.json());
      } catch (error) {
        console.error('AI insights error:', error);
      } finally {
        setLoadingAI(false);
      }
    };

    fetchAllAIInsights();
  }, []);

  return (
    <MainLayout title="Overview">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* AI Insights Header */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl shadow-lg p-6 lg:col-span-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <SparklesIcon className="w-8 h-8 text-white" />
              <div>
                <h2 className="text-2xl font-bold text-white">AI-Powered Financial Intelligence</h2>
                <p className="text-blue-100">Real-time predictions from advanced machine learning models</p>
              </div>
            </div>
            <a
              href="/ai-insights"
              className="px-4 py-2 bg-white text-blue-600 rounded-lg font-medium hover:bg-blue-50 transition-colors"
            >
              View All Features
            </a>
          </div>
        </div>

        {loadingAI ? (
          <div className="lg:col-span-2 flex items-center justify-center py-12 bg-white rounded-xl">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-blue-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Loading AI predictions...</p>
            </div>
          </div>
        ) : recentTransactions.length === 0 ? (
          <div className="lg:col-span-2 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl shadow-lg p-8 border-2 border-dashed border-blue-200">
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
                <SparklesIcon className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">AI Insights Not Available Yet</h3>
              <p className="text-gray-600 mb-4 max-w-md mx-auto">
                Start by creating transactions, budgets, and goals. Our AI will analyze your financial data and provide personalized insights.
              </p>
              <div className="flex gap-4 justify-center">
                <a href="/transactions" className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
                  <CurrencyDollarIcon className="w-5 h-5" />
                  Add Transaction
                </a>
                <a href="/budgets" className="inline-flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition">
                  <ChartBarIcon className="w-5 h-5" />
                  Create Budget
                </a>
              </div>
            </div>
          </div>
        ) : (
          <>
            {/* Transaction Type Prediction Dashboard */}
            <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-blue-600">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="p-3 bg-blue-50 rounded-lg">
                    <CurrencyDollarIcon className="w-6 h-6 text-blue-600" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-gray-800">Transaction Prediction</h3>
                    <p className="text-sm text-gray-600">AI-powered transaction analysis</p>
                  </div>
                </div>
              </div>
              {transactionPrediction ? (
                <div className="space-y-3">
                  <div className="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Predicted Type</span>
                    <span className="text-lg font-bold text-blue-600">
                      {transactionPrediction.predicted_type || 'EXPENSE'}
                    </span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Confidence</span>
                    <span className="text-lg font-bold text-blue-600">
                      {((transactionPrediction.confidence || 0.85) * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Category</span>
                    <span className="text-sm font-semibold text-gray-800">
                      {transactionPrediction.category || 'Shopping'}
                    </span>
                  </div>
                  {transactionPrediction.details && (
                    <div className="mt-2 p-3 bg-gray-50 rounded-lg">
                      <p className="text-xs text-gray-600">Model: {transactionPrediction.details.model || 'TabNet Ensemble'}</p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-4 text-gray-500">
                  <p>No data available</p>
                </div>
              )}
            </div>

            {/* Budget Risk Analysis Dashboard */}
            <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-purple-600">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="p-3 bg-purple-50 rounded-lg">
                    <ChartBarIcon className="w-6 h-6 text-purple-600" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-gray-800">Budget Risk Analysis</h3>
                    <p className="text-sm text-gray-600">Overspending risk prediction</p>
                  </div>
                </div>
              </div>
              {budgetRisk ? (
                <div className="space-y-3">
                  <div className="flex justify-between items-center p-3 bg-purple-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Risk Level</span>
                    <span className={`text-lg font-bold ${
                      budgetRisk.risk_level === 'HIGH' ? 'text-red-600' :
                      budgetRisk.risk_level === 'MEDIUM' ? 'text-orange-600' : 'text-green-600'
                    }`}>
                      {budgetRisk.risk_level || 'LOW'}
                    </span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-purple-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Overrun Probability</span>
                    <span className="text-lg font-bold text-purple-600">
                      {((budgetRisk.overrun_probability || 0.25) * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-purple-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Budget Usage</span>
                    <span className="text-sm font-semibold text-gray-800">
                      {budgetRisk.usage_percentage || '85'}%
                    </span>
                  </div>
                  {budgetRisk.recommendation && (
                    <div className="mt-2 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                      <p className="text-xs text-yellow-800 font-medium">💡 {budgetRisk.recommendation}</p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-4 text-gray-500">
                  <p>No data available</p>
                </div>
              )}
            </div>

            {/* Goal Success Prediction Dashboard */}
            <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-green-600">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="p-3 bg-green-50 rounded-lg">
                    <ArrowTrendingUpIcon className="w-6 h-6 text-green-600" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-gray-800">Goal Success Prediction</h3>
                    <p className="text-sm text-gray-600">Savings goal achievement</p>
                  </div>
                </div>
              </div>
              {goalSuccess ? (
                <div className="space-y-3">
                  <div className="flex justify-between items-center p-3 bg-green-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Success Probability</span>
                    <span className="text-lg font-bold text-green-600">
                      {((goalSuccess.success_probability || 0.78) * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-green-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Current Progress</span>
                    <span className="text-lg font-bold text-green-600">
                      {goalSuccess.progress_percentage || '70'}%
                    </span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-green-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Status</span>
                    <span className={`text-sm font-semibold ${
                      goalSuccess.status === 'ON_TRACK' ? 'text-green-600' : 'text-orange-600'
                    }`}>
                      {goalSuccess.status || 'ON_TRACK'}
                    </span>
                  </div>
                  {goalSuccess.recommendation && (
                    <div className="mt-2 p-3 bg-green-50 border border-green-200 rounded-lg">
                      <p className="text-xs text-green-800 font-medium">✨ {goalSuccess.recommendation}</p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-4 text-gray-500">
                  <p>No data available</p>
                </div>
              )}
            </div>

            {/* Fraud Detection Dashboard */}
            <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-red-600">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="p-3 bg-red-50 rounded-lg">
                    <ShieldExclamationIcon className="w-6 h-6 text-red-600" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-gray-800">Fraud Detection</h3>
                    <p className="text-sm text-gray-600">Transaction security analysis</p>
                  </div>
                </div>
              </div>
              {fraudDetection ? (
                <div className="space-y-3">
                  <div className="flex justify-between items-center p-3 bg-red-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Fraud Status</span>
                    <span className={`text-lg font-bold ${
                      fraudDetection.is_fraudulent ? 'text-red-600' : 'text-green-600'
                    }`}>
                      {fraudDetection.is_fraudulent ? '⚠️ FLAGGED' : '✅ SECURE'}
                    </span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-red-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Risk Score</span>
                    <span className="text-lg font-bold text-red-600">
                      {((fraudDetection.fraud_score || 0.05) * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-red-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Risk Level</span>
                    <span className={`text-sm font-semibold ${
                      fraudDetection.risk_level === 'HIGH' ? 'text-red-600' :
                      fraudDetection.risk_level === 'MEDIUM' ? 'text-orange-600' : 'text-green-600'
                    }`}>
                      {fraudDetection.risk_level || 'LOW'}
                    </span>
                  </div>
                  {fraudDetection.alert_message && (
                    <div className={`mt-2 p-3 ${
                      fraudDetection.is_fraudulent ? 'bg-red-50 border border-red-200' : 'bg-green-50 border border-green-200'
                    } rounded-lg`}>
                      <p className={`text-xs font-medium ${
                        fraudDetection.is_fraudulent ? 'text-red-800' : 'text-green-800'
                      }`}>
                        🛡️ {fraudDetection.alert_message}
                      </p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-4 text-gray-500">
                  <p>No data available</p>
                </div>
              )}
            </div>
          </>
        )}

        {/* Primary Card */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-800">Your Cards</h2>
            <a
              href="/cards"
              className="text-sm text-blue-600 hover:underline"
            >
              {userCards.length > 0 ? 'See All' : 'Add Card'}
            </a>
          </div>
          {userCards.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p>No cards added yet. Click "Add Card" to get started!</p>
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-4">
              {userCards.map((card, index) => (
                <CreditCard
                  key={card.id || index}
                  balance={`E£ ${card.balance || '0.00'}`}
                  cardHolder={card.institution_name || 'Card'}
                  cardNumber={`**** **** **** ${card.token?.slice(-4) || '****'}`}
                />
              ))}
            </div>
          )}
        </div>

        {/* Recent Transaction */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-800">Recent Transactions</h2>
            <a
              href="/transactions"
              className="text-sm text-blue-600 hover:underline"
            >
              {recentTransactions.length > 0 ? 'See All' : 'Add Transaction'}
            </a>
          </div>
          {recentTransactions.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p>No transactions yet. Start adding transactions to see them here!</p>
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
                        {txn.type === 'INCOME' ? '💰' : '💳'}
                      </span>
                    </div>
                    <div>
                      <div className="font-medium text-gray-800">{txn.description || 'Transaction'}</div>
                      <div className="text-sm text-gray-500">
                        {new Date(txn.date || txn.created_at).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                  <div className={`font-semibold ${txn.type === 'INCOME' ? 'text-green-600' : 'text-red-600'}`}>
                    {txn.type === 'INCOME' ? '+' : '-'}E£{Math.abs(txn.amount).toFixed(2)}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Weekly Activity */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Weekly Activity</h2>
          {weeklyActivity.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p>No activity data yet. Data will appear as you make transactions!</p>
            </div>
          ) : (
            <>
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
            </>
          )}
        </div>

        {/* Expense Statistics */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Expense Statistics</h2>
          {expenseStats.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p>No expense data yet. Statistics will appear as you add expenses!</p>
            </div>
          ) : (
            <PieChart data={expenseStats} size={180} />
          )}
        </div>

        {/* Balance History */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Balance History</h2>
          {balanceHistory.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p>No balance history yet. Data will build up over time!</p>
            </div>
          ) : (
            <LineChart data={balanceHistory} height={200} color="#3b82f6" />
          )}
        </div>

        {/* Quick Transfer - Removed fake recipients */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Quick Transfer</h2>
          <div className="text-center py-8 text-gray-500">
            <p>Transfer feature coming soon! You can manage transfers from the transactions page.</p>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
