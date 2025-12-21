'use client';

import { useState, useEffect, useRef } from 'react';
import { MagnifyingGlassIcon, BellIcon, UserCircleIcon, Cog6ToothIcon } from '@heroicons/react/24/outline';
import { useRouter } from 'next/navigation';
import api from '../../lib/api';


interface HeaderProps {
  title: string;
}

export default function Header({ title }: HeaderProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);
  const searchTimeout = useRef<number | null>(null);
  const cancelTokenRef = useRef<any>(null);
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchQuery)}`);
    }
  };

  // Real-time search (debounced)
  useEffect(() => {
    if (searchTimeout.current) {
      window.clearTimeout(searchTimeout.current);
      searchTimeout.current = null;
    }

    if (!searchQuery.trim()) {
      setSearchResults([]);
      setShowDropdown(false);
      return;
    }

    setSearchLoading(true);
    searchTimeout.current = window.setTimeout(async () => {
      try {
        if (cancelTokenRef.current) {
          cancelTokenRef.current.cancel('new-request');
        }
        const CancelToken = (await import('axios')).default.CancelToken;
        cancelTokenRef.current = CancelToken.source();
        const res = await api.get(`/search/`, {
          params: { q: searchQuery },
          cancelToken: cancelTokenRef.current.token,
        });
        setSearchResults(Array.isArray(res.data) ? res.data : res.data.results || []);
        setShowDropdown(true);
      } catch (err: any) {
        if (err?.__CANCEL__) return;
        setSearchResults([]);
        setShowDropdown(true);
      } finally {
        setSearchLoading(false);
      }
    }, 300);

    return () => {
      if (searchTimeout.current) {
        window.clearTimeout(searchTimeout.current);
      }
    };
  }, [searchQuery]);

  const [user, setUser] = useState<any | null>(null);
  const [isAdmin, setIsAdmin] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await api.get('/auth/profile/');
        setUser(res.data.user || null);
        setIsAdmin(!!res.data.is_admin);
      } catch (err) {
        setUser(null);
        setIsAdmin(false);
      }
    };
    fetchProfile();
  }, []);

  const handleLogout = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
    setUser(null);
    setIsAdmin(false);
    router.push('/login');
  };

  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-800">{title}</h1>
        
        <div className="flex items-center gap-4">
          <form onSubmit={handleSearch} className="relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onFocus={() => { if (searchResults.length) setShowDropdown(true); }}
              placeholder="Search for something"
              className="pl-10 pr-4 py-2 w-64 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            {showDropdown && (
              <div className="absolute left-0 mt-2 w-80 bg-white border rounded-md shadow-lg z-50 max-h-72 overflow-auto">
                {searchLoading ? (
                  <div className="p-3 text-sm text-gray-500">Loading...</div>
                ) : searchResults.length === 0 ? (
                  <div className="p-3 text-sm text-gray-500">No results</div>
                ) : (
                  searchResults.map((r, idx) => (
                    <button
                      key={idx}
                      onClick={() => {
                        setShowDropdown(false);
                        setSearchQuery('');
                        // try to navigate to item link if available
                        const path = r.url || r.link || r.path || `/search?q=${encodeURIComponent(r.title || r.name || '')}`;
                        router.push(path);
                      }}
                      className="w-full text-left px-4 py-2 hover:bg-gray-100"
                    >
                      <div className="text-sm font-medium">{r.title || r.name || r.label || JSON.stringify(r)}</div>
                      {r.description && <div className="text-xs text-gray-500">{r.description}</div>}
                    </button>
                  ))
                )}
              </div>
            )}
          </form>
          
          <div className="flex items-center gap-3">
            <button
              onClick={() => router.push('/settings')}
              className="p-2 hover:bg-gray-100 rounded-lg"
              title="Settings"
            >
              <Cog6ToothIcon className="w-5 h-5 text-gray-600" />
            </button>
            <button
              onClick={() => alert('You have 3 new notifications')}
              className="p-2 hover:bg-gray-100 rounded-lg relative"
              title="Notifications"
            >
              <BellIcon className="w-5 h-5 text-gray-600" />
              <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>
            <div className="relative">
              {user ? (
                <>
                  <button
                    onClick={() => setMenuOpen((s) => !s)}
                    className="p-2 hover:bg-gray-100 rounded-lg flex items-center gap-2"
                    title="Profile"
                  >
                    <div className="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center font-medium">
                      {((user.first_name || user.email || 'U')[0] || 'U').toUpperCase()}
                    </div>
                  </button>
                  {menuOpen && (
                    <div className="absolute right-0 mt-2 w-48 bg-white border rounded-md shadow-lg z-50">
                      <button
                        onClick={() => { setMenuOpen(false); router.push('/settings/profile/edit'); }}
                        className="w-full text-left px-4 py-2 hover:bg-gray-100"
                      >
                        Edit Profile
                      </button>
                      {isAdmin && (
                        <button
                          onClick={() => { setMenuOpen(false); window.location.href = '/admin/'; }}
                          className="w-full text-left px-4 py-2 hover:bg-gray-100"
                        >
                          Admin Dashboard
                        </button>
                      )}
                      <button
                        onClick={() => { setMenuOpen(false); handleLogout(); }}
                        className="w-full text-left px-4 py-2 hover:bg-gray-100 text-red-600"
                      >
                        Logout
                      </button>
                    </div>
                  )}
                </>
              ) : (
                <button onClick={() => router.push('/login')} className="px-3 py-1 bg-blue-600 text-white rounded">Sign in</button>
              )}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
