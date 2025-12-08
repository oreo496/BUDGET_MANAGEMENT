'use client';

import { useState } from 'react';
import MainLayout from '@/components/Layout/MainLayout';

export default function Chatbot() {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState<Array<{role: string, content: string}>>([]);

  const suggestedActions = [
    'budgeting strategy',
    'calculations',
    'app support',
    'send your receipt',
  ];

  const handleSend = () => {
    if (!message.trim()) return;
    
    const userMessage = message;
    setMessage('');
    
    // Add user message to history
    setChatHistory([...chatHistory, { role: 'user', content: userMessage }]);
    
    // Simulate bot response
    setTimeout(() => {
      const responses: {[key: string]: string} = {
        'budgeting strategy': 'Here are some budgeting tips: 1) Track all expenses, 2) Set monthly limits, 3) Review weekly, 4) Save 20% of income.',
        'calculations': 'I can help with financial calculations! What would you like to calculate? (Interest, savings, loan payments, etc.)',
        'app support': 'For app support, please contact our support team at support@funder.com or check our FAQ section.',
        'send your receipt': 'To send a receipt, go to Transactions page, select a transaction, and click "Upload Receipt".',
      };
      
      const response = responses[userMessage.toLowerCase()] || 
        `I understand you're asking about "${userMessage}". How can I help you with that?`;
      
      setChatHistory(prev => [...prev, { role: 'assistant', content: response }]);
    }, 1000);
  };

  const handleSuggestedAction = (action: string) => {
    setMessage(action);
  };

  return (
    <MainLayout title="Chat bot">
      <div className="flex items-center justify-center min-h-[calc(100vh-200px)]">
        <div className="w-full max-w-2xl">
          <div className="text-center mb-12">
            <h1 className="text-6xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-4">
              Hello
            </h1>
          </div>
          
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="relative mb-6">
              <button
                onClick={() => setMessage('')}
                className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                title="Clear"
              >
                <span className="text-2xl">+</span>
              </button>
              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder="tell me what you have in mind..."
                className="w-full pl-12 pr-32 py-4 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-blue-500 text-lg"
              />
              <button
                onClick={handleSend}
                className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:opacity-90 transition-opacity flex items-center gap-2"
              >
                send <span>→</span>
              </button>
            </div>
            
            <div className="flex flex-wrap gap-3 mb-6">
              {suggestedActions.map((action, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestedAction(action)}
                  className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm font-medium text-gray-700 transition-colors"
                >
                  {action}
                </button>
              ))}
            </div>

            {/* Chat History */}
            {chatHistory.length > 0 && (
              <div className="space-y-4 max-h-96 overflow-y-auto">
                {chatHistory.map((msg, index) => (
                  <div
                    key={index}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] p-3 rounded-lg ${
                        msg.role === 'user'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {msg.content}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </MainLayout>
  );
}

