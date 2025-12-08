import MainLayout from '@/components/Layout/MainLayout';
import LineChart from '@/components/Charts/LineChart';

export default function Investments() {
  const yearlyInvestment = [
    { label: '2016', value: 10000 },
    { label: '2017', value: 15000 },
    { label: '2018', value: 25000 },
    { label: '2019', value: 38000 },
    { label: '2020', value: 32000 },
    { label: '2021', value: 30000 },
  ];

  const monthlyRevenue = [
    { label: '2016', value: 8000 },
    { label: '2017', value: 12000 },
    { label: '2018', value: 18000 },
    { label: '2019', value: 25000 },
    { label: '2020', value: 28000 },
    { label: '2021', value: 32000 },
  ];

  return (
    <MainLayout title="Investments">
      <div className="space-y-6">
        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">💰</span>
              </div>
              <div>
                <div className="text-sm text-gray-500">Total Invested Amount</div>
                <div className="text-2xl font-bold text-gray-800">E£150,000</div>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-pink-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">📊</span>
              </div>
              <div>
                <div className="text-sm text-gray-500">Number of Investments</div>
                <div className="text-2xl font-bold text-gray-800">1,250</div>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">↻</span>
              </div>
              <div>
                <div className="text-sm text-gray-500">Rate of Return</div>
                <div className="text-2xl font-bold text-green-600">+5.80%</div>
              </div>
            </div>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Yearly Total Investment</h2>
            <LineChart data={yearlyInvestment} height={250} color="#f97316" />
          </div>
          
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Monthly Revenue</h2>
            <LineChart data={monthlyRevenue} height={250} color="#14b8a6" />
          </div>
        </div>

        {/* Investment Tables */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">My Investment</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                    <span className="text-xl">🍎</span>
                  </div>
                  <div>
                    <div className="font-semibold text-gray-800">Apple Store</div>
                    <div className="text-sm text-gray-500">E-commerce, Marketplace</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm text-gray-500">Investment Value</div>
                  <div className="font-semibold text-gray-800">E£54,000</div>
                  <div className="text-sm text-green-600 font-semibold">+16%</div>
                </div>
              </div>
              
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                    <span className="text-xl">G</span>
                  </div>
                  <div>
                    <div className="font-semibold text-gray-800">Samsung Mobile</div>
                    <div className="text-sm text-gray-500">E-commerce, Marketplace</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm text-gray-500">Investment Value</div>
                  <div className="font-semibold text-gray-800">E£25,300</div>
                  <div className="text-sm text-red-600 font-semibold">-4%</div>
                </div>
              </div>
              
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                    <span className="text-xl">T</span>
                  </div>
                  <div>
                    <div className="font-semibold text-gray-800">Tesla Motors</div>
                    <div className="text-sm text-gray-500">Electric Vehicles</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm text-gray-500">Investment Value</div>
                  <div className="font-semibold text-gray-800">E£8,200</div>
                  <div className="text-sm text-green-600 font-semibold">+25%</div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Trending Stock</h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <span className="text-lg font-bold text-gray-400">01.</span>
                  <div>
                    <div className="font-semibold text-gray-800">Trivago</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-semibold text-gray-800">E£520</div>
                  <div className="text-sm text-green-600 font-semibold">+5%</div>
                </div>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <span className="text-lg font-bold text-gray-400">02.</span>
                  <div>
                    <div className="font-semibold text-gray-800">Canon</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-semibold text-gray-800">E£480</div>
                  <div className="text-sm text-green-600 font-semibold">+10%</div>
                </div>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <span className="text-lg font-bold text-gray-400">03.</span>
                  <div>
                    <div className="font-semibold text-gray-800">Uber Food</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-semibold text-gray-800">E£350</div>
                  <div className="text-sm text-red-600 font-semibold">-3%</div>
                </div>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <span className="text-lg font-bold text-gray-400">04.</span>
                  <div>
                    <div className="font-semibold text-gray-800">Nokia</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-semibold text-gray-800">E£940</div>
                  <div className="text-sm text-green-600 font-semibold">+2%</div>
                </div>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <span className="text-lg font-bold text-gray-400">05.</span>
                  <div>
                    <div className="font-semibold text-gray-800">Tiktok</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-semibold text-gray-800">E£670</div>
                  <div className="text-sm text-red-600 font-semibold">-12%</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

