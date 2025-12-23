'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';
import api from '../../lib/api';

export default function LoginPage() {
  const router = useRouter();
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [pendingCreds, setPendingCreds] = useState<{ identifier: string; password: string } | null>(null);
  const [mfaRequired, setMfaRequired] = useState(false);
  const [mfaToken, setMfaToken] = useState('');
  const [backupCode, setBackupCode] = useState('');
  const [smsOtpRequired, setSmsOtpRequired] = useState(false);
  const [smsOtpCode, setSmsOtpCode] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const idToUse = pendingCreds?.identifier || identifier;
      const passwordToUse = pendingCreds?.password || password;

      // If SMS OTP is required, verify the code
      if (smsOtpRequired) {
        const payload = {
          identifier: idToUse,
          password: passwordToUse,
          code: smsOtpCode,
        };
        const res = await api.post('/auth/sms-otp/verify/', payload);
        const token = res.data.token;
        if (token && typeof window !== 'undefined') {
          localStorage.setItem('token', token);
        }
        setSmsOtpRequired(false);
        setSmsOtpCode('');
        setPendingCreds(null);
        router.push('/');
        return;
      }

      const payload: Record<string, string> = { password: passwordToUse };
      if (idToUse.includes('@')) {
        payload.email = idToUse;
      }
      payload.username = idToUse;

      if (mfaRequired) {
        if (mfaToken) payload.mfa_token = mfaToken;
        if (backupCode) payload.backup_code = backupCode;
      }

      const res = await api.post('/auth/login/', payload);
      if (res.data?.mfa_required || res.data?.requires_mfa) {
        setMfaRequired(true);
        setPendingCreds({ identifier: idToUse, password: passwordToUse });
        setError('MFA required. Enter your 6-digit TOTP code or a backup code.');
        return;
      }

      const token = res.data.token;
      if (token && typeof window !== 'undefined') {
        localStorage.setItem('token', token);
      }
      setMfaRequired(false);
      setMfaToken('');
      setBackupCode('');
      setPendingCreds(null);
      router.push('/');
    } catch (err: any) {
      const status = err?.response?.status;
      const errorData = err?.response?.data;
      
      if (status === 402 && errorData?.sms_otp_required) {
        setSmsOtpRequired(true);
        setPendingCreds({ identifier, password });
        setError(errorData?.message || 'SMS OTP verification required. Check your phone for the 6-digit code.');
      } else if (errorData?.error) {
        setError(errorData.error);
      } else if (errorData?.detail) {
        setError(errorData.detail);
      } else if (err?.message?.includes('Network Error')) {
        setError('Unable to connect to server. Please ensure the backend is running.');
      } else {
        setError('Login failed. Please check your credentials and try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleRequestSms = async () => {
    setError(null);
    try {
      const payload = { identifier, password };
      const res = await api.post('/auth/sms-otp/request/', payload);
      setError(res.data?.message || 'SMS OTP sent to your phone.');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to send SMS OTP. Try again.');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-12 bg-white p-6 rounded-md shadow">
      <h2 className="text-2xl font-semibold mb-4">Sign in</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm">Email or Username</label>
          <input
            value={identifier}
            onChange={(e) => setIdentifier(e.target.value)}
            disabled={mfaRequired || smsOtpRequired}
            placeholder="jane@doe.com or janedoe"
            className="w-full border px-3 py-2 rounded"
          />
        </div>
        <div>
          <label className="block text-sm">Password</label>
          <div className="relative">
            <input
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              type={showPassword ? 'text' : 'password'}
              disabled={mfaRequired && !!pendingCreds}
              className="w-full border px-3 py-2 rounded"
            />
            <button
              type="button"
              onClick={() => setShowPassword(s => !s)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
            >
              {showPassword ? <EyeSlashIcon className="w-5 h-5" /> : <EyeIcon className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {mfaRequired && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div>
              <label className="block text-sm">TOTP Code</label>
              <input
                value={mfaToken}
                onChange={(e) => setMfaToken(e.target.value)}
                placeholder="6-digit code"
                className="w-full border px-3 py-2 rounded"
              />
            </div>
            <div>
              <label className="block text-sm">Backup Code (optional)</label>
              <input
                value={backupCode}
                onChange={(e) => setBackupCode(e.target.value)}
                placeholder="8-character backup"
                className="w-full border px-3 py-2 rounded"
              />
            </div>
          </div>
        )}

        {smsOtpRequired && (
          <div>
            <label className="block text-sm">SMS OTP Code</label>
            <input
              value={smsOtpCode}
              onChange={(e) => setSmsOtpCode(e.target.value)}
              placeholder="6-digit code from SMS"
              className="w-full border px-3 py-2 rounded"
              autoFocus
            />
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <svg className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div className="flex-1">
                <p className="text-sm font-medium text-red-800">{error}</p>
              </div>
            </div>
          </div>
        )}

        <div className="flex items-center justify-between gap-2">
          <button disabled={loading} className="bg-blue-600 text-white px-4 py-2 rounded flex-1">
            {loading ? 'Signing in...' : smsOtpRequired ? 'Verify OTP' : mfaRequired ? 'Verify MFA' : 'Sign in'}
          </button>
          {!smsOtpRequired && !mfaRequired && (
            <button
              type="button"
              onClick={handleRequestSms}
              disabled={!identifier || !password || loading}
              className="text-xs text-blue-600 underline hover:text-blue-700 whitespace-nowrap"
            >
              SMS OTP
            </button>
          )}
        </div>

        <a href="/register" className="block text-sm text-blue-600 text-center">
          Create account
        </a>
      </form>
    </div>
  );
}
