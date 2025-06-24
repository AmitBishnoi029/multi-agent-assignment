import React, { useState } from 'react';
import axios from 'axios';

export default function Dashboard() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [agent, setAgent] = useState('support');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    try {
      const endpoint = agent === 'support' ? '/ask-support' : '/ask-dashboard';
      const res = await axios.post(`http://localhost:8000${endpoint}`, {
        query,
      });
      setResponse(res.data.response);
    } catch (err) {
      setResponse('Error: Unable to reach backend');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-2xl mx-auto bg-white shadow-xl rounded-2xl p-6">
        <h1 className="text-2xl font-bold mb-4">Multi-Agent Assistant</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Query
            </label>
            <input
              type="text"
              className="mt-1 block w-full border rounded-md p-2"
              placeholder="Enter Here"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>

          <div className="flex gap-4 items-center">
            <label>
              <input
                type="radio"
                value="support"
                checked={agent === 'support'}
                onChange={() => setAgent('support')}
              />{' '}
              Support Agent
            </label>
            <label>
              <input
                type="radio"
                value="dashboard"
                checked={agent === 'dashboard'}
                onChange={() => setAgent('dashboard')}
              />{' '}
              Dashboard Agent
            </label>
          </div>

          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            {loading ? 'Sending...' : 'Send Query'}
          </button>
        </form>

        {response && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold">Response:</h2>
            <div className="mt-2 whitespace-pre-wrap bg-gray-50 p-4 rounded border">
              {response}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
