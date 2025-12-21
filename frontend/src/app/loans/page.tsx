"use client";

import MainLayout from '@/components/Layout/MainLayout';
import { useEffect, useState } from 'react';
import api from '@/lib/api';

export default function Loans() {
  const [loans, setLoans] = useState<any[]>([]);
  const [amount, setAmount] = useState('');
  const [lender, setLender] = useState('');
  const [term, setTerm] = useState('12');
  const [interest, setInterest] = useState('5.0');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchLoans = async () => {
    try {
      const res = await api.get('/loans/');
      // Ensure we always have an array
      const data = res.data;
      if (Array.isArray(data)) {
        setLoans(data);
      } else if (data && Array.isArray(data.results)) {
        setLoans(data.results);
      } else if (data && typeof data === 'object') {
        // If data is an object but not an array, wrap it
        setLoans([data]);
      } else {
        setLoans([]);
      }
    } catch (err) {
      console.error('Error fetching loans:', err);
      setLoans([]);
    }
  };

  useEffect(() => {
    fetchLoans();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await api.post('/loans/', {
        amount: parseFloat(amount),
        lender_name: lender || 'Funder Bank',
        term_months: parseInt(term, 10),
        interest_rate: parseFloat(interest),
      });
      setAmount('');
      setLender('');
      setTerm('12');
      setInterest('5.0');
      await fetchLoans();
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to create loan');
    } finally {
      setLoading(false);
    }
  };

  return (
    <MainLayout title="Loans">
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Loans</h2>
        <form onSubmit={handleCreate} className="grid grid-cols-1 md:grid-cols-5 gap-3 mb-4">
          <input value={amount} onChange={(e) => setAmount(e.target.value)} placeholder="Amount" className="border px-3 py-2 rounded" required />
          <input value={lender} onChange={(e) => setLender(e.target.value)} placeholder="Lender Name" className="border px-3 py-2 rounded" />
          <input value={term} onChange={(e) => setTerm(e.target.value)} placeholder="Term (months)" className="border px-3 py-2 rounded" required />
          <input value={interest} onChange={(e) => setInterest(e.target.value)} placeholder="Interest %" className="border px-3 py-2 rounded" required />
          <div>
            <button disabled={loading} className="bg-blue-600 text-white px-4 py-2 rounded">{loading ? 'Creating...' : 'Create Loan'}</button>
          </div>
        </form>
        {error && <div className="text-red-600 mb-4">{error}</div>}

        <h3 className="font-medium mb-2">Your loans</h3>
        {loans.length === 0 ? (
          <div className="text-gray-600">No loans found.</div>
        ) : (
          <ul className="space-y-2">
            {loans.map((l: any) => (
              <li key={l.id} className="border p-3 rounded">
                <div className="flex justify-between">
                  <div>
                    <div className="font-medium">{l.lender_name || 'Funder Bank'}</div>
                    <div className="font-medium">Amount: ${l.amount}</div>
                    <div className="text-sm text-gray-600">Term: {l.term_months} months • Interest: {l.interest_rate}%</div>
                  </div>
                  <div className="text-sm text-gray-500">{l.status}</div>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </MainLayout>
  );
}

