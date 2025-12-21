'use client';

import { useState, useEffect } from 'react';
import MainLayout from '@/components/Layout/MainLayout';
import CreditCard from '@/components/Cards/CreditCard';
import PieChart from '@/components/Charts/PieChart';
import api from '@/lib/api';

export default function Cards() {
  const [cards, setCards] = useState<any[]>([]);
  const [cardType, setCardType] = useState('Classic');
  const [expirationDate, setExpirationDate] = useState('');
  const [cardNumber, setCardNumber] = useState('');
  const [cardName, setCardName] = useState('');
  const [loading, setLoading] = useState(false);

  // Get tomorrow's date as minimum date
  const getTomorrowDate = () => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    return tomorrow.toISOString().split('T')[0];
  };

  useEffect(() => {
    fetchCards();
  }, []);

  const fetchCards = async () => {
    try {
      const res = await api.get('/bank-accounts/');
      setCards(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      console.error('Error fetching cards:', err);
      setCards([]);
    }
  };

  const formatCardNumber = (value: string) => {
    // Remove all non-digit characters
    const cleaned = value.replace(/\D/g, '');
    // Limit to 16 digits
    const limited = cleaned.slice(0, 16);
    // Add space every 4 digits
    const formatted = limited.match(/.{1,4}/g)?.join(' ') || limited;
    return formatted;
  };

  const handleCardNumberChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const formatted = formatCardNumber(e.target.value);
    setCardNumber(formatted);
  };

  const handleAddCard = async () => {
    const cleanCardNumber = cardNumber.replace(/\s/g, '');
    if (!cleanCardNumber || cleanCardNumber.length !== 16) {
      alert('Please enter a valid 16-digit card number');
      return;
    }
    if (!cardName.trim()) {
      alert('Please enter a name for the card');
      return;
    }
    if (!expirationDate) {
      alert('Please select an expiration date');
      return;
    }

    setLoading(true);
    try {
      await api.post('/bank-accounts/', {
        institution_name: cardName,
        account_type: cardType,
        token: cleanCardNumber
      });
      setCardNumber('');
      setCardName('');
      setCardType('Classic');
      setExpirationDate('');
      await fetchCards();
      alert('Card added successfully!');
    } catch (err: any) {
      console.error('Error adding card:', err);
      const errorMsg = err?.response?.data?.detail || 
                      err?.response?.data?.user?.[0] || 
                      err?.response?.data?.token?.[0] ||
                      'Failed to add card';
      alert(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  // Group cards by institution for pie chart
  const cardExpenseStats = cards.reduce((acc: any[], card: any) => {
    const existing = acc.find((item: any) => item.label === card.institution_name);
    if (existing) {
      existing.value += 1;
    } else {
      acc.push({
        label: card.institution_name || 'Unknown',
        value: 1,
        color: `#${Math.floor(Math.random() * 16777215).toString(16)}`,
      });
    }
    return acc;
  }, []);

  return (
    <MainLayout title="Credit Cards">
      <div className="space-y-6">
        {/* Primary Cards Section */}
        {cards.length > 0 && (
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Your Cards</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {cards.slice(0, 3).map((card, idx) => (
                <CreditCard
                  key={card.id || idx}
                  balance="E£ ****.**"
                  cardHolder={card.institution_name}
                  validThru="**/**"
                  cardNumber={`**** **** **** ****`}
                />
              ))}
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Card Statistics */}
          {cards.length > 0 && (
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-lg font-semibold text-gray-800 mb-4">Card Distribution</h2>
              <PieChart data={cardExpenseStats} size={200} />
            </div>
          )}

          {/* Card List */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Card List</h2>
            {cards.length === 0 ? (
              <div className="text-gray-600 text-center py-8">
                No cards added yet. Add your first card below.
              </div>
            ) : (
              <div className="space-y-4">
                {cards.map((card, idx) => (
                  <div key={card.id || idx} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                        <span className="text-blue-600 text-xl">💳</span>
                      </div>
                      <div>
                        <div className="text-sm text-gray-500">Card Type: {card.account_type || 'Standard'}</div>
                        <div className="font-semibold text-gray-800">{card.institution_name || 'Bank'}</div>
                        <div className="text-sm text-gray-600">Added: {new Date(card.created_at).toLocaleDateString()}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Add New Card */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Add New Card</h2>
            <p className="text-sm text-gray-600 mb-6">
              Securely add your credit or debit card information to your account.
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
                    <option>Titanium</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Bank Name</label>
                  <input
                    type="text"
                    value={cardName}
                    onChange={(e) => setCardName(e.target.value)}
                    placeholder="e.g., CIB Bank"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Card Number</label>
                  <input
                    type="text"
                    value={cardNumber}
                    onChange={handleCardNumberChange}
                    placeholder="**** **** **** ****"
                    maxLength={19}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono"
                  />
                  <p className="text-xs text-gray-500 mt-1">{cardNumber.replace(/\s/g, '').length}/16 digits</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Expiration Date</label>
                  <input
                    type="date"
                    value={expirationDate}
                    onChange={(e) => setExpirationDate(e.target.value)}
                    min={getTomorrowDate()}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <p className="text-xs text-gray-500 mt-1">Must be after today</p>
                </div>
              </div>
              <button
                onClick={handleAddCard}
                disabled={loading}
                className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:bg-gray-400"
              >
                {loading ? 'Adding Card...' : 'Add Card'}
              </button>
            </div>
          </div>

          {/* Card Settings */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Card Settings</h2>
            <div className="space-y-4">
              <button
                onClick={() => {
                  if (cards.length === 0) {
                    alert('No cards to remove');
                    return;
                  }
                  if (confirm('Are you sure you want to remove the last card?')) {
                    // Implement delete functionality
                    alert('Card removal feature coming soon');
                  }
                }}
                className="w-full flex items-center gap-3 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <span className="text-xl">💳</span>
                <div className="flex-1 text-left">
                  <div className="font-semibold text-gray-800">Manage Cards</div>
                  <div className="text-sm text-gray-500">View and manage your saved cards</div>
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
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

