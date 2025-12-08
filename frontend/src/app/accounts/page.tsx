import MainLayout from '@/components/Layout/MainLayout';
import CreditCard from '@/components/Cards/CreditCard';
import BarChart from '@/components/Charts/BarChart';

export default function Accounts() {
  const debitCreditData = [
    { label: 'Sat', value: 1200, color: '#3b82f6' },
    { label: 'Sun', value: 800, color: '#f97316' },
    { label: 'Mon', value: 1500, color: '#3b82f6' },
    { label: 'Tue', value: 2000, color: '#f97316' },
    { label: 'Wed', value: 900, color: '#3b82f6' },
    { label: 'Thu', value: 1100, color: '#f97316' },
    { label: 'Fri', value: 1800, color: '#3b82f6' },
  ];

  return (
    <MainLayout title="Accounts">
      <div className="space-y-6">
        {/* Financial Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">💰</span>
              </div>
              <div>
                <div className="text-sm text-gray-500">My Balance</div>
                <div className="text-2xl font-bold text-gray-800">E£12,750</div>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">💵</span>
              </div>
              <div>
                <div className="text-sm text-gray-500">Income</div>
                <div className="text-2xl font-bold text-gray-800">E£5,600</div>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">🏢</span>
              </div>
              <div>
                <div className="text-sm text-gray-500">Expense</div>
                <div className="text-2xl font-bold text-gray-800">E£3,460</div>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">🐷</span>
              </div>
              <div>
                <div className="text-sm text-gray-500">Total Saving</div>
                <div className="text-2xl font-bold text-gray-800">E£7,920</div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Last Transaction */}
          <div className="lg:col-span-1 bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Last Transaction</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                    <span className="text-green-600 text-xl">🎵</span>
                  </div>
                  <div>
                    <div className="font-medium text-gray-800">Spotify Subscription</div>
                    <div className="text-xs text-gray-500">25 Jan 2021 • Shopping</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-xs text-yellow-600 mb-1">Pending</div>
                  <div className="text-red-600 font-semibold">-E£150</div>
                </div>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-blue-600 text-xl">🔧</span>
                  </div>
                  <div>
                    <div className="font-medium text-gray-800">Mobile Service</div>
                    <div className="text-xs text-gray-500">25 Jan 2021 • Service</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-xs text-green-600 mb-1">Completed</div>
                  <div className="text-red-600 font-semibold">-E£340</div>
                </div>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-pink-100 rounded-full flex items-center justify-center">
                    <span className="text-pink-600 text-xl">👤</span>
                  </div>
                  <div>
                    <div className="font-medium text-gray-800">Emily Wilson</div>
                    <div className="text-xs text-gray-500">25 Jan 2021 • Transfer</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-xs text-green-600 mb-1">Completed</div>
                  <div className="text-green-600 font-semibold">+E£780</div>
                </div>
              </div>
            </div>
          </div>

          {/* My Card */}
          <div className="lg:col-span-1 bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-800">My Card</h2>
              <a href="#" className="text-sm text-blue-600 hover:underline">+Edit Card</a>
            </div>
            <CreditCard
              balance="E£ 273,907.37"
              cardHolder="Mohamed Elhosieny"
              validThru="07/28"
              cardNumber="3778 **** **** 1234"
            />
          </div>

          {/* Debit & Credit Overview */}
          <div className="lg:col-span-1 bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Debit & Credit Overview</h2>
            <p className="text-sm text-gray-600 mb-4">$7,560 Debited & $5,420 Credited in this Week</p>
            <div className="flex items-center gap-4 mb-4">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-blue-600 rounded"></div>
                <span className="text-sm text-gray-600">Debit</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-orange-500 rounded"></div>
                <span className="text-sm text-gray-600">Credit</span>
              </div>
            </div>
            <BarChart data={debitCreditData} height={200} />
          </div>
        </div>

        {/* Invoices Sent */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Invoices Sent</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                  <span className="text-green-600 text-xl">🍎</span>
                </div>
                <div>
                  <div className="font-medium text-gray-800">Apple Store</div>
                  <div className="text-xs text-gray-500">5h ago</div>
                </div>
              </div>
              <div className="text-lg font-semibold text-gray-800">E£450</div>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-orange-100 rounded-full flex items-center justify-center">
                  <span className="text-orange-600 text-xl">👤</span>
                </div>
                <div>
                  <div className="font-medium text-gray-800">Michael</div>
                  <div className="text-xs text-gray-500">2 days ago</div>
                </div>
              </div>
              <div className="text-lg font-semibold text-gray-800">E£160</div>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                  <span className="text-blue-600 text-xl">🎮</span>
                </div>
                <div>
                  <div className="font-medium text-gray-800">Playstation</div>
                  <div className="text-xs text-gray-500">5 days ago</div>
                </div>
              </div>
              <div className="text-lg font-semibold text-gray-800">E£1085</div>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-pink-100 rounded-full flex items-center justify-center">
                  <span className="text-pink-600 text-xl">👤</span>
                </div>
                <div>
                  <div className="font-medium text-gray-800">William</div>
                  <div className="text-xs text-gray-500">10 days ago</div>
                </div>
              </div>
              <div className="text-lg font-semibold text-gray-800">E£90</div>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

