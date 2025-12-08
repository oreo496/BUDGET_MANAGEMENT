'use client';

import { useState } from 'react';
import { MagnifyingGlassIcon, BellIcon, UserCircleIcon, Cog6ToothIcon } from '@heroicons/react/24/outline';
import { useRouter } from 'next/navigation';


interface HeaderProps {
  title: string;
}

export default function Header({ title }: HeaderProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      alert(`Searching for: ${searchQuery}`);
      // In real app: router.push(`/search?q=${searchQuery}`);
    }
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
              placeholder="Search for something"
              className="pl-10 pr-4 py-2 w-64 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
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
            <button
              onClick={() => alert('Profile menu')}
              className="p-2 hover:bg-gray-100 rounded-lg"
              title="Profile"
            >
              <UserCircleIcon className="w-8 h-8 text-gray-600" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
