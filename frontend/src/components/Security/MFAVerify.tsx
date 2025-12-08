'use client';

import { useState } from 'react';
import api from '@/lib/api';

interface MFAVerifyProps {
  onVerify: (token: string) => void;
  onCancel: () => void;
}

export default function MFAVerify({ onVerify, onCancel }: MFAVerifyProps) {
  const [token, setToken] = useState('');
  const [backupCode, setBackupCode] = useState('');
  const [useBackupCode, setUseBackupCode] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleVerify = async () => {
    if (!useBackupCode && (!token || token.length !== 6)) {
      setError('Please enter a 6-digit code');
      return;
    }

    if (useBackupCode && (!backupCode || backupCode.length !== 8)) {
      setError('Please enter an 8-digit backup code');
      return;
    }

    setLoading(true);
    setError('');

    try {
      onVerify(useBackupCode ? backupCode : token);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Verification failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 max-w-md mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Multi-Factor Authentication</h2>
      
      <p className="text-gray-600 mb-6">
        Enter the 6-digit code from your authenticator app:
      </p>

      {!useBackupCode ? (
        <div className="mb-6">
          <input
            type="text"
            value={token}
            onChange={(e) => setToken(e.target.value.replace(/\D/g, '').slice(0, 6))}
            placeholder="000000"
            maxLength={6}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-center text-2xl tracking-widest"
          />
        </div>
      ) : (
        <div className="mb-6">
          <input
            type="text"
            value={backupCode}
            onChange={(e) => setBackupCode(e.target.value.replace(/\D/g, '').slice(0, 8))}
            placeholder="00000000"
            maxLength={8}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-center text-xl tracking-widest"
          />
        </div>
      )}

      <div className="mb-6">
        <button
          onClick={() => setUseBackupCode(!useBackupCode)}
          className="text-sm text-blue-600 hover:underline"
        >
          {useBackupCode ? 'Use authenticator code instead' : 'Use backup code instead'}
        </button>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {error}
        </div>
      )}

      <div className="flex gap-3">
        <button
          onClick={handleVerify}
          disabled={loading || (!useBackupCode && token.length !== 6) || (useBackupCode && backupCode.length !== 8)}
          className="flex-1 bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50"
        >
          {loading ? 'Verifying...' : 'Verify'}
        </button>
        <button
          onClick={onCancel}
          className="px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
        >
          Cancel
        </button>
      </div>
    </div>
  );
}

