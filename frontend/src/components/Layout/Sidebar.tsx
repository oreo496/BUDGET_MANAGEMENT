'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  HomeIcon,
  DocumentTextIcon,
  UserIcon,
  BuildingOfficeIcon,
  CreditCardIcon,
  BanknotesIcon,
  ChatBubbleLeftRightIcon,
  HeartIcon,
  Cog6ToothIcon,
  SparklesIcon,
  BellIcon,
  TrophyIcon,
} from '@heroicons/react/24/outline';

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Transactions', href: '/transactions', icon: DocumentTextIcon },
  { name: 'Accounts', href: '/accounts', icon: UserIcon },
  { name: 'Investments', href: '/investments', icon: BuildingOfficeIcon },
  { name: 'Cards', href: '/cards', icon: CreditCardIcon },
  { name: 'Loans', href: '/loans', icon: BanknotesIcon },
  { name: 'Goals', href: '/goals', icon: TrophyIcon },
  { name: 'AI Insights', href: '/ai-insights', icon: SparklesIcon },
  { name: 'Notifications', href: '/notifications', icon: BellIcon },
  { name: 'Chat bot', href: '/chatbot', icon: ChatBubbleLeftRightIcon },
  { name: 'My Privileges', href: '/privileges', icon: HeartIcon },
  { name: 'Setting', href: '/settings', icon: Cog6ToothIcon },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="flex flex-col w-64 bg-gray-50 border-r border-gray-200">
      <div className="flex items-center gap-2 p-6">
        <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
          <span className="text-white font-bold text-xl">F</span>
        </div>
        <span className="text-xl font-bold text-gray-800">FUNDER</span>
      </div>
      
      <nav className="flex-1 px-4 py-4 space-y-1">
        {navigation.map((item) => {
          const isActive = pathname === item.href || 
            (item.href !== '/' && pathname?.startsWith(item.href));
          
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-blue-50 text-blue-600 border-l-4 border-blue-600'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <item.icon className="w-5 h-5" />
              <span className="font-medium">{item.name}</span>
            </Link>
          );
        })}
      </nav>
    </div>
  );
}

