'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import MainLayout from '@/components/Layout/MainLayout';
import {
  SparklesIcon,
  ChartBarIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ArrowTrendingUpIcon,
  CurrencyDollarIcon,
  ShieldExclamationIcon,
} from '@heroicons/react/24/outline';

export default function AIInsightsPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [transactionPrediction, setTransactionPrediction] = useState<any>(null);
  const [budgetRisk, setBudgetRisk] = useState<any>(null);
  const [goalSuccess, setGoalSuccess] = useState<any>(null);
  const [fraudDetection, setFraudDetection] = useState<any>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }
    fetchAllPredictions();
  }, [router]);

  const fetchAllPredictions = async () => {
    setLoading(true);
    const token = localStorage.getItem('token');

    try {
      // Fetch real AI predictions from the backend
      const [txnRes, budgetRes, goalRes, fraudRes] = await Promise.all([
        fetch('http://localhost:8000/api/ai-alerts/predict/transaction/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({}),
        }).catch(() => null),
        
        fetch('http://localhost:8000/api/ai-alerts/predict/budget-risk/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({}),
        }).catch(() => null),
        
        fetch('http://localhost:8000/api/ai-alerts/predict/goal-success/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({}),
        }).catch(() => null),
        
        fetch('http://localhost:8000/api/ai-alerts/predict/flagged/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({}),
        }).catch(() => null),
      ]);

      if (txnRes?.ok) setTransactionPrediction(await txnRes.json());
      if (budgetRes?.ok) setBudgetRisk(await budgetRes.json());
      if (goalRes?.ok) setGoalSuccess(await goalRes.json());
      if (fraudRes?.ok) setFraudDetection(await fraudRes.json());
    } catch (error: any) {
      console.error('Error fetching predictions:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading && !transactionPrediction && !budgetRisk && !goalSuccess && !fraudDetection) {
    return (
      <MainLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-blue-600 mx-auto mb-4"></div>
            <div className="text-gray-500">Loading AI Insights...</div>
          </div>
        </div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl shadow-lg p-6">
          <div className="flex items-center gap-3">
            <SparklesIcon className="w-8 h-8 text-white" />
            <div>
              <h1 className="text-2xl font-bold text-white">AI-Powered Financial Intelligence</h1>
              <p className="text-blue-100">Real-time predictions from advanced machine learning models</p>
            </div>
          </div>
        </div>

        {/* Refresh Button */}
        <div className="flex justify-end">
          <button
            onClick={fetchAllPredictions}
            disabled={loading}
            className={`px-6 py-2 rounded-lg font-medium transition-colors ${
              loading
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {loading ? 'Refreshing...' : '🔄 Refresh Predictions'}
          </button>
        </div>

        {/* AI Dashboards Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Transaction Prediction Dashboard */}
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
              <div className="text-center py-8 text-gray-500">
                <p>Loading prediction...</p>
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
              <div className="text-center py-8 text-gray-500">
                <p>Loading prediction...</p>
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
              <div className="text-center py-8 text-gray-500">
                <p>Loading prediction...</p>
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
              <div className="text-center py-8 text-gray-500">
                <p>Loading prediction...</p>
              </div>
            )}
          </div>
        </div>

        {/* Info Section */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <div className="flex items-start gap-3">
            <SparklesIcon className="w-6 h-6 text-blue-600 flex-shrink-0" />
            <div>
              <h3 className="font-semibold text-blue-900">About AI Models</h3>
              <p className="text-sm text-blue-800 mt-2">
                Our AI models use advanced machine learning algorithms including TabNet, DNN, and
                Attention mechanisms to provide accurate predictions. The models are trained on
                historical financial data and continuously improve over time.
              </p>
              <ul className="mt-3 space-y-1 text-sm text-blue-800">
                <li>• Transaction predictions use ensemble models for better accuracy</li>
                <li>• Budget risk analysis considers spending patterns and trends</li>
                <li>• Goal predictions evaluate progress and historical success rates</li>
                <li>• Fraud detection uses anomaly detection and pattern recognition</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
