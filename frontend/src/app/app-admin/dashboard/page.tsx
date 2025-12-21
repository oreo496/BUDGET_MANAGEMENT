"use client";

import { useEffect, useState } from 'react';
import api from '../../../../lib/api';

export default function AdminDashboard() {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const token = typeof window !== 'undefined' ? localStorage.getItem('app_admin_token') : null;
        if (!token) {
          window.location.href = '/app-admin/login';
          return;
        }
        const res = await api.get('/admin/dashboard/', { headers: { Authorization: `Bearer ${token}` } });
        setData(res.data);
      } catch (err: any) {
        setError(err?.response?.data?.detail || 'Failed to load dashboard');
      }
    };
    load();
  }, []);

  const handleLogout = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('app_admin_token');
      window.location.href = '/app-admin/login';
    }
  };

  return (
    <div className="max-w-2xl mx-auto mt-8 bg-white p-6 rounded shadow">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">Admin Dashboard</h2>
        <button onClick={handleLogout} className="text-sm text-red-600">Logout</button>
      </div>
      {error && <div className="text-red-600">{error}</div>}
      {data ? (
        <div className="grid grid-cols-3 gap-4">
          <div className="p-4 border rounded">Users<br /><span className="text-2xl font-bold">{data.users}</span></div>
          <div className="p-4 border rounded">Loans<br /><span className="text-2xl font-bold">{data.loans}</span></div>
          <div className="p-4 border rounded">Transactions<br /><span className="text-2xl font-bold">{data.transactions}</span></div>
        </div>
      ) : (
        <div>Loading...</div>
      )}
    </div>
  );
}
