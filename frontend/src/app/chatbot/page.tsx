'use client';

import { useState } from 'react';
import MainLayout from '@/components/Layout/MainLayout';
import { apiGet } from '@/lib/api';

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000/api';

export default function Chatbot() {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState<Array<{role: string, content: string}>>([]);
  const [loading, setLoading] = useState(false);

  const suggestedActions = [
    'budgeting strategy',
    'calculations',
    'app support',
    'send your receipt',
  ];

  const handleSend = async () => {
    if (!message.trim()) return;
    
    const userMessage = message;
    setMessage('');
    
    // Add user message to history
    setChatHistory([...chatHistory, { role: 'user', content: userMessage }]);
    
    // Call backend API
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/chatbot/messages/send_message/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage }),
      });
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      const data = await response.json();
      setChatHistory(prev => [...prev, { role: 'assistant', content: data.bot_response }]);
    } catch (err: any) {
      console.error('Chatbot error:', err);
      setChatHistory(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error processing your message. Please try again.' 
      }]);
    } finally {
      setLoading(false);
    }
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

