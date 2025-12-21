import React, { useEffect, useState } from 'react';

interface Transaction {
  id: string;
  amount: number;
  type: 'INCOME' | 'EXPENSE';
  merchant?: string;
  date: string;
  flagged_fraud: boolean;
  ai_alert_message?: string | null;
}

export default function AIInsights() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch('/api/transactions');
        if (!res.ok) throw new Error('Failed to fetch transactions');
        const data = await res.json();
        setTransactions(data);
      } catch (e: any) {
        setError(e.message || 'Unknown error');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div>Loading AI insights...</div>;
  if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;

  const flagged = transactions.filter(t => t.flagged_fraud);

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">AI Insights</h2>
      {flagged.length === 0 ? (
        <p>No flagged transactions.</p>
      ) : (
        <ul className="space-y-2">
          {flagged.map(tx => (
            <li key={tx.id} className="border rounded p-3">
              <div className="flex justify-between">
                <span>
                  {tx.type}: ${Number(tx.amount).toFixed(2)} {tx.merchant ? `- ${tx.merchant}` : ''}
                </span>
                <span className="text-sm text-red-600">Flagged Fraud</span>
              </div>
              {tx.ai_alert_message && (
                <div className="mt-2 text-sm text-gray-700">{tx.ai_alert_message.replace(/^txn:[^|]+\s\|\s/, '')}</div>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
