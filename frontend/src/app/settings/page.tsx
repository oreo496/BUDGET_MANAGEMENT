'use client';

import { useState, useEffect } from 'react';
import MainLayout from '@/components/Layout/MainLayout';
import api from '@/lib/api';

export default function Settings() {
  const [activeTab, setActiveTab] = useState<'preferences' | 'security'>('preferences');
  const [currency, setCurrency] = useState('EGP');
  const [timezone, setTimezone] = useState('(UTC+2:00) Cairo');
  const [notifications, setNotifications] = useState({
    digitalCurrency: true,
    merchantOrder: false,
    recommendations: true,
  });
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [mfaEnabled, setMfaEnabled] = useState(false);
  const [showMfaSetup, setShowMfaSetup] = useState(false);
  const [mfaData, setMfaData] = useState<{ qr_code: string; backup_codes: string[]; secret: string } | null>(null);
  const [mfaToken, setMfaToken] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    // Fetch current MFA status
    const fetchMfaStatus = async () => {
      try {
        const res = await api.get('/auth/mfa/status/');
        setMfaEnabled(res.data.mfa_enabled);
      } catch (err) {
        console.error('Failed to fetch MFA status:', err);
      }
    };
    fetchMfaStatus();
  }, []);

  const handleEnableMfa = async () => {
    setError(null);
    setSuccess(null);
    setLoading(true);
    try {
      const res = await api.post('/auth/mfa/setup/');
      setMfaData(res.data);
      setShowMfaSetup(true);
    } catch (err: any) {
      setError(err?.response?.data?.error || 'Failed to setup MFA');
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyMfa = async () => {
    if (!mfaToken || !mfaData) return;
    setError(null);
    setSuccess(null);
    setLoading(true);
    try {
      await api.post('/auth/mfa/verify-setup/', {
        token: mfaToken,
        secret: mfaData.secret
      });
      setMfaEnabled(true);
      setShowMfaSetup(false);
      setMfaToken('');
      setSuccess('MFA enabled successfully!');
    } catch (err: any) {
      setError(err?.response?.data?.error || 'Invalid token. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDisableMfa = async () => {
    const password = prompt('Enter your password to disable MFA:');
    if (!password) return;
    
    setError(null);
    setSuccess(null);
    setLoading(true);
    try {
      await api.post('/auth/mfa/disable/', { password });
      setMfaEnabled(false);
      setSuccess('MFA disabled successfully');
    } catch (err: any) {
      setError(err?.response?.data?.error || 'Failed to disable MFA');
    } finally {
      setLoading(false);
    }
  };


  return (
    <MainLayout title="Setting">
      <div className="max-w-4xl">
        <div className="bg-white rounded-xl shadow-sm p-6">
          {/* Tabs */}
          <div className="flex gap-4 border-b border-gray-200 mb-6">
            <button
              onClick={() => setActiveTab('preferences')}
              className={`px-4 py-2 font-medium transition-colors ${
                activeTab === 'preferences'
                  ? 'text-blue-600 border-b-2 border-blue-600'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              Preferences
            </button>
            <button
              onClick={() => setActiveTab('security')}
              className={`px-4 py-2 font-medium transition-colors ${
                activeTab === 'security'
                  ? 'text-blue-600 border-b-2 border-blue-600'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              Security
            </button>
          </div>

          {/* Preferences Tab Content */}
          {activeTab === 'preferences' && (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Currency</label>
                <input
                  type="text"
                  value={currency}
                  onChange={(e) => setCurrency(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Time Zone</label>
                <select
                  value={timezone}
                  onChange={(e) => setTimezone(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option>(UTC+2:00) Cairo</option>
                  <option>(UTC+0:00) London</option>
                  <option>(UTC-5:00) New York</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-4">Notification</label>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-700">I send or receive digita currency</span>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={notifications.digitalCurrency}
                        onChange={(e) => setNotifications({ ...notifications, digitalCurrency: e.target.checked })}
                        className="sr-only peer"
                      />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-gray-700">I receive merchant order</span>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={notifications.merchantOrder}
                        onChange={(e) => setNotifications({ ...notifications, merchantOrder: e.target.checked })}
                        className="sr-only peer"
                      />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-gray-700">There are recommendation for my account</span>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={notifications.recommendations}
                        onChange={(e) => setNotifications({ ...notifications, recommendations: e.target.checked })}
                        className="sr-only peer"
                      />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>
                </div>
              </div>

              <div className="flex justify-end">
                <button
                  onClick={() => {
                    alert(`Settings saved!\nCurrency: ${currency}\nTimezone: ${timezone}\nNotifications: ${JSON.stringify(notifications)}`);
                  }}
                  className="bg-blue-600 text-white px-8 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors"
                >
                  Save
                </button>
              </div>
            </div>
          )}

          {/* Security Tab Content */}
          {activeTab === 'security' && (
            <div className="space-y-6">
              {/* Change Password Section */}
              <div className="border-b border-gray-200 pb-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Change Password</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Current Password</label>
                    <input
                      type="password"
                      value={currentPassword}
                      onChange={(e) => setCurrentPassword(e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Enter current password"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">New Password</label>
                    <input
                      type="password"
                      value={newPassword}
                      onChange={(e) => setNewPassword(e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Enter new password"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Confirm New Password</label>
                    <input
                      type="password"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Confirm new password"
                    />
                  </div>
                  <button
                    onClick={() => {
                      if (!currentPassword || !newPassword || !confirmPassword) {
                        alert('Please fill all password fields');
                        return;
                      }
                      if (newPassword !== confirmPassword) {
                        alert('New passwords do not match');
                        return;
                      }
                      if (newPassword.length < 8) {
                        alert('Password must be at least 8 characters long');
                        return;
                      }
                      alert('Password changed successfully!');
                      setCurrentPassword('');
                      setNewPassword('');
                      setConfirmPassword('');
                    }}
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors"
                  >
                    Change Password
                  </button>
                </div>
              </div>

              {/* Two-Factor Authentication Section */}
              <div className="border-b border-gray-200 pb-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Two-Factor Authentication</h3>
                
                {error && (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
                    <p className="text-sm text-red-800">{error}</p>
                  </div>
                )}
                
                {success && (
                  <div className="bg-green-50 border border-green-200 rounded-lg p-3 mb-4">
                    <p className="text-sm text-green-800">{success}</p>
                  </div>
                )}
                
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <p className="text-gray-700 font-medium">2FA Status</p>
                    <p className="text-sm text-gray-500">
                      {mfaEnabled ? 'Enabled - Your account is protected' : 'Disabled - Add extra security'}
                    </p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={mfaEnabled}
                      disabled={loading}
                      onChange={(e) => {
                        if (e.target.checked) {
                          handleEnableMfa();
                        } else {
                          handleDisableMfa();
                        }
                      }}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>
                
                {showMfaSetup && mfaData && (
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <p className="text-sm text-blue-800 mb-3 font-semibold">
                      Step 1: Scan QR Code
                    </p>
                    <p className="text-xs text-blue-700 mb-3">
                      Use Google Authenticator, Authy, or any TOTP authenticator app
                    </p>
                    <div className="flex justify-center mb-4 bg-white p-4 rounded-lg">
                      <img 
                        src={mfaData.qr_code} 
                        alt="MFA QR Code" 
                        className="w-48 h-48"
                      />
                    </div>
                    
                    <p className="text-sm text-blue-800 mb-2 font-semibold">
                      Step 2: Backup Codes
                    </p>
                    <p className="text-xs text-blue-700 mb-2">
                      Save these codes in a safe place. Each can be used once if you lose access to your authenticator.
                    </p>
                    <div className="bg-white p-3 rounded border border-blue-300 mb-4 font-mono text-sm">
                      {mfaData.backup_codes.map((code, idx) => (
                        <div key={idx} className="text-gray-700">{code}</div>
                      ))}
                    </div>
                    
                    <p className="text-sm text-blue-800 mb-2 font-semibold">
                      Step 3: Verify
                    </p>
                    <p className="text-xs text-blue-700 mb-2">
                      Enter the 6-digit code from your authenticator app
                    </p>
                    <input
                      type="text"
                      value={mfaToken}
                      onChange={(e) => setMfaToken(e.target.value)}
                      placeholder="123456"
                      maxLength={6}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg mb-3 text-center text-2xl tracking-widest"
                    />
                    
                    <div className="flex gap-2">
                      <button
                        onClick={handleVerifyMfa}
                        disabled={loading || mfaToken.length !== 6}
                        className="flex-1 bg-blue-600 text-white py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:bg-gray-400"
                      >
                        {loading ? 'Verifying...' : 'Verify & Enable'}
                      </button>
                      <button
                        onClick={() => {
                          setShowMfaSetup(false);
                          setMfaData(null);
                          setMfaToken('');
                        }}
                        disabled={loading}
                        className="flex-1 bg-gray-200 text-gray-700 py-2 rounded-lg font-medium hover:bg-gray-300 transition-colors"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {/* Session Management */}
              <div className="border-b border-gray-200 pb-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Active Sessions</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-medium text-gray-800">Current Session</p>
                      <p className="text-sm text-gray-500">Windows • Chrome • Cairo, Egypt</p>
                      <p className="text-xs text-gray-400">Last active: Just now</p>
                    </div>
                    <span className="px-3 py-1 bg-green-100 text-green-700 text-sm rounded-full">Active</span>
                  </div>
                </div>
              </div>

              {/* Security Notifications */}
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Security Notifications</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-700">Email notifications for new logins</span>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        defaultChecked
                        className="sr-only peer"
                      />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-700">Alert me about suspicious activity</span>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        defaultChecked
                        className="sr-only peer"
                      />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </MainLayout>
  );
}

