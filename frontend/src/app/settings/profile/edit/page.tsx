'use client';

import { useEffect, useState } from 'react';
import api from '../../../../lib/api';

export default function EditProfile() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [phone, setPhone] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pwCurrent, setPwCurrent] = useState('');
  const [pwNew, setPwNew] = useState('');
  const [pwConfirm, setPwConfirm] = useState('');
  const [pwLoading, setPwLoading] = useState(false);
  const [pwError, setPwError] = useState<string | null>(null);
  const [pwSuccess, setPwSuccess] = useState<string | null>(null);
  const [showPw, setShowPw] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await api.get('/auth/profile/');
        const user = res.data.user;
          const adminFlag = res.data.is_admin;
        if (user) {
          setFirstName(user.first_name || '');
          setLastName(user.last_name || '');
          setPhone(user.phone || '');
            setIsAdmin(Boolean(adminFlag));
        }
      } catch (err) {
        // ignore
      }
    };
    fetchProfile();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await api.put('/auth/profile/update/', {
        first_name: firstName,
        last_name: lastName,
        phone,
      });
      // Optionally show success
      window.alert('Profile updated');
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Update failed');
    } finally {
      setLoading(false);
    }
  };

  const pwPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/;
  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setPwError(null);
    setPwSuccess(null);
    if (!pwCurrent || !pwNew || !pwConfirm) {
      setPwError('All password fields are required');
      return;
    }
    if (pwNew !== pwConfirm) {
      setPwError('New password and confirm do not match');
      return;
    }
    if (!pwPattern.test(pwNew)) {
      setPwError('Password must be at least 8 chars and include uppercase, lowercase, number and special character');
      return;
    }
    setPwLoading(true);
    try {
      const res = await api.post('/auth/profile/change-password/', {
        current_password: pwCurrent,
        new_password: pwNew,
      });
      setPwSuccess(res.data.detail || 'Password changed');
      setPwCurrent(''); setPwNew(''); setPwConfirm('');
    } catch (err: any) {
      setPwError(err?.response?.data?.detail || 'Password change failed');
    } finally {
      setPwLoading(false);
    }
  };

  return (
    <div className="max-w-lg mx-auto mt-8 bg-white p-6 rounded shadow">
      <h2 className="text-xl font-semibold mb-4">Edit Profile</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm">First name</label>
          <input value={firstName} onChange={(e) => setFirstName(e.target.value)} className="w-full border px-3 py-2 rounded" />
        </div>
        <div>
          <label className="block text-sm">Last name</label>
          <input value={lastName} onChange={(e) => setLastName(e.target.value)} className="w-full border px-3 py-2 rounded" />
        </div>
        <div>
          <label className="block text-sm">Phone</label>
          <input value={phone} onChange={(e) => setPhone(e.target.value)} className="w-full border px-3 py-2 rounded" />
        </div>
        {error && <div className="text-red-600">{error}</div>}
        <div>
          <button disabled={loading} className="bg-blue-600 text-white px-4 py-2 rounded">{loading ? 'Saving...' : 'Save changes'}</button>
        </div>
      </form>
        <div className="max-w-lg mx-auto mt-8 bg-white p-6 rounded shadow">
          <h2 className="text-xl font-semibold mb-4">My privileges</h2>
          <div className="mb-4">
            <div className="text-sm">Admin: {isAdmin ? 'Yes' : 'No'}</div>
          </div>
          {isAdmin && (
            <div className="mb-2">
              <a href="/app-admin/login" className="text-blue-600 underline">Open Admin Dashboard</a>
            </div>
          )}
        </div>

        <div className="max-w-lg mx-auto mt-4 bg-white p-6 rounded shadow">
        <h2 className="text-xl font-semibold mb-4">Security</h2>
        <form onSubmit={handlePasswordChange} className="space-y-4">
          <div>
            <label className="block text-sm">Current password</label>
            <input value={pwCurrent} onChange={(e) => setPwCurrent(e.target.value)} type={showPw ? 'text' : 'password'} className="w-full border px-3 py-2 rounded" />
          </div>
          <div>
            <label className="block text-sm">New password</label>
            <input value={pwNew} onChange={(e) => setPwNew(e.target.value)} type={showPw ? 'text' : 'password'} className="w-full border px-3 py-2 rounded" />
          </div>
          <div>
            <label className="block text-sm">Confirm new password</label>
            <input value={pwConfirm} onChange={(e) => setPwConfirm(e.target.value)} type={showPw ? 'text' : 'password'} className="w-full border px-3 py-2 rounded" />
          </div>
          <div className="flex items-center gap-3">
            <label className="text-sm flex items-center gap-2"><input type="checkbox" checked={showPw} onChange={() => setShowPw(s => !s)} /> Show passwords</label>
          </div>
          {pwError && <div className="text-red-600">{pwError}</div>}
          {pwSuccess && <div className="text-green-600">{pwSuccess}</div>}
          <div>
            <button disabled={pwLoading} className="bg-blue-600 text-white px-4 py-2 rounded">{pwLoading ? 'Saving...' : 'Change password'}</button>
          </div>
        </form>
      </div>
    </div>
  );
}
