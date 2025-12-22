import MainLayout from '@/components/Layout/MainLayout';

export default function Investments() {
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
                <div className="text-2xl font-bold text-gray-800">E£0.00</div>
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
                <div className="text-2xl font-bold text-gray-800">0</div>
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
                <div className="text-2xl font-bold text-gray-500">0.00%</div>
              </div>
            </div>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Yearly Total Investment</h2>
            <div className="flex items-center justify-center h-64 text-gray-400">
              <div className="text-center">
                <div className="text-4xl mb-2">📈</div>
                <p>No investment data yet</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Monthly Revenue</h2>
            <div className="flex items-center justify-center h-64 text-gray-400">
              <div className="text-center">
                <div className="text-4xl mb-2">💹</div>
                <p>No revenue data yet</p>
              </div>
            </div>
          </div>
        </div>

        {/* Investment Tables */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">My Investment</h2>
            <div className="flex items-center justify-center h-64 text-gray-400">
              <div className="text-center">
                <div className="text-4xl mb-2">💼</div>
                <p className="mb-2">No investments yet</p>
                <p className="text-sm">Investment feature coming soon!</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Trending Stock</h2>
            <div className="flex items-center justify-center h-64 text-gray-400">
              <div className="text-center">
                <div className="text-4xl mb-2">📊</div>
                <p className="mb-2">No stock data available</p>
                <p className="text-sm">Stock tracking feature coming soon!</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

