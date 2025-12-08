'use client';

import { useState } from 'react';
import MainLayout from '@/components/Layout/MainLayout';
import CreditCard from '@/components/Cards/CreditCard';
import PieChart from '@/components/Charts/PieChart';

export default function Cards() {
  const [cardType, setCardType] = useState('Classic');
  const [expirationDate, setExpirationDate] = useState('25 January 2025');

  const cardExpenseStats = [
    { label: 'CIB Bank', value: 35, color: '#14b8a6' },
    { label: 'QNB Bank', value: 25, color: '#60a5fa' },
    { label: 'HSBC Bank', value: 20, color: '#ec4899' },
    { label: 'ADIB Bank', value: 20, color: '#f97316' },
  ];

  return (
    <MainLayout title="Credit Cards">
      <div className="space-y-6">
        {/* Primary Card Section */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Primary Card</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <CreditCard
              balance="E£ 273,907.37"
              cardHolder="Mohamed Elhosieny"
              validThru="07/28"
              cardNumber="3778 **** **** 1234"
            />
            <CreditCard
              balance="E£ 273,907.37"
              cardNumber="3778 **** **** 1234"
              showCVV
            />
            <div className="bg-white border-2 border-gray-200 rounded-xl p-6 flex flex-col items-center justify-center">
              <div className="text-3xl font-bold text-green-600 mb-2">QNB</div>
              <div className="text-sm text-gray-600 mb-4">titanium card</div>
              <div className="text-lg font-mono tracking-wider text-gray-800">3778 **** **** 1234</div>
              <label className="relative inline-flex items-center cursor-pointer mt-4">
                <input type="checkbox" className="sr-only peer" defaultChecked />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Card Expense Statistics */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Card Expense Statistics</h2>
            <PieChart data={cardExpenseStats} size={200} />
          </div>

          {/* Card List */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Card List</h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <span className="text-blue-600 text-xl">💳</span>
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">Card Type: Secondary</div>
                    <div className="font-semibold text-gray-800">CIB Bank</div>
                    <div className="text-sm text-gray-600">Card Number: **** 5600</div>
                    <div className="text-sm text-gray-600">Name: William</div>
                  </div>
                </div>
                <button
                  onClick={() => alert(`Viewing details for ${item.bank || 'Card'}`)}
                  className="text-blue-600 hover:underline text-sm"
                >
                  View Details
                </button>
              </div>
              
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                    <span className="text-orange-600 text-xl">💳</span>
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">Card Type: Secondary</div>
                    <div className="font-semibold text-gray-800">ADIB Bank</div>
                    <div className="text-sm text-gray-600">Card Number: **** 5600</div>
                    <div className="text-sm text-gray-600">Name: Edward</div>
                  </div>
                </div>
                <button
                  onClick={() => alert(`Viewing details for ${item.bank || 'Card'}`)}
                  className="text-blue-600 hover:underline text-sm"
                >
                  View Details
                </button>
              </div>
              
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-pink-100 rounded-lg flex items-center justify-center">
                    <span className="text-pink-600 text-xl">💳</span>
                  </div>
                  <div>
                    <div className="text-sm text-gray-500">Card Type: Secondary</div>
                    <div className="font-semibold text-gray-800">HSBC Bank</div>
                    <div className="text-sm text-gray-600">Card Number: **** 5600</div>
                    <div className="text-sm text-gray-600">Name: Michel</div>
                  </div>
                </div>
                <button
                  onClick={() => alert(`Viewing details for ${item.bank || 'Card'}`)}
                  className="text-blue-600 hover:underline text-sm"
                >
                  View Details
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Add New Card */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Add New Card</h2>
            <p className="text-sm text-gray-600 mb-6">
              Credit Card generally means a plastic card issued by Scheduled Commercial Banks assigned to a Cardholder, 
              with a credit limit, that can be used to purchase goods and services on credit or obtain cash advances.
            </p>
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Card Type</label>
                  <select
                    value={cardType}
                    onChange={(e) => setCardType(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option>Classic</option>
                    <option>Gold</option>
                    <option>Platinum</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Name On Card</label>
                  <input
                    type="text"
                    defaultValue="My Cards"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Card Number</label>
                  <input
                    type="text"
                    placeholder="**** **** **** ****"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Expiration Date</label>
                  <select
                    value={expirationDate}
                    onChange={(e) => setExpirationDate(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option>25 January 2025</option>
                    <option>26 January 2025</option>
                    <option>27 January 2025</option>
                  </select>
                </div>
              </div>
              <button
                onClick={() => {
                  const cardNumber = (document.querySelector('input[placeholder="**** **** **** ****"]') as HTMLInputElement)?.value;
                  const nameOnCard = (document.querySelector('input[defaultValue="My Cards"]') as HTMLInputElement)?.value;
                  
                  if (!cardNumber || cardNumber.length < 16) {
                    alert('Please enter a valid card number');
                    return;
                  }
                  
                  alert(`Card added successfully!\nType: ${cardType}\nName: ${nameOnCard || 'My Cards'}\nCard: ${cardNumber}\nExpires: ${expirationDate}`);
                }}
                className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors"
              >
                Add Card
              </button>
            </div>
          </div>

          {/* Card Setting */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Card Setting</h2>
            <div className="space-y-4">
              <button
                onClick={() => {
                  if (confirm('Are you sure you want to remove this card?')) {
                    alert('Card removed successfully');
                  }
                }}
                className="w-full flex items-center gap-3 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <span className="text-xl">💳</span>
                <div className="flex-1 text-left">
                  <div className="font-semibold text-gray-800">Remove Card</div>
                  <div className="text-sm text-gray-500">Instantly remove your card</div>
                </div>
              </button>
              
              <button
                onClick={() => {
                  const newPin = prompt('Enter new 4-digit PIN:');
                  if (newPin && /^\d{4}$/.test(newPin)) {
                    alert('PIN changed successfully');
                  } else if (newPin) {
                    alert('PIN must be 4 digits');
                  }
                }}
                className="w-full flex items-center gap-3 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <span className="text-xl">🔒</span>
                <div className="flex-1 text-left">
                  <div className="font-semibold text-gray-800">Change Pin Code</div>
                  <div className="text-sm text-gray-500">Choose another pin code</div>
                </div>
              </button>
              
              <button
                onClick={() => alert('Adding card to Google Pay...')}
                className="w-full flex items-center gap-3 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <span className="text-xl font-bold text-blue-600">G</span>
                <div className="flex-1 text-left">
                  <div className="font-semibold text-gray-800">Add to Google Pay</div>
                  <div className="text-sm text-gray-500">Withdraw without any card</div>
                </div>
              </button>
              
              <button
                onClick={() => alert('Adding card to Apple Pay...')}
                className="w-full flex items-center gap-3 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <span className="text-xl">🍎</span>
                <div className="flex-1 text-left">
                  <div className="font-semibold text-gray-800">Add to Apple Pay</div>
                  <div className="text-sm text-gray-500">Withdraw without any card</div>
                </div>
              </button>
              
              <button
                onClick={() => alert('Adding card to Apple Store...')}
                className="w-full flex items-center gap-3 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <span className="text-xl">🍎</span>
                <div className="flex-1 text-left">
                  <div className="font-semibold text-gray-800">Add to Apple Store</div>
                  <div className="text-sm text-gray-500">Withdraw without any card</div>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

