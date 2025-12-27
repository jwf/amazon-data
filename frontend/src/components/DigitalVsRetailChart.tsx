import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { getDigitalVsRetail, DigitalVsRetail } from '../api';

const DigitalVsRetailChart: React.FC = () => {
  const [data, setData] = useState<DigitalVsRetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState<'orders' | 'spending'>('spending');

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const result = await getDigitalVsRetail();
        setData(result);
      } catch (error) {
        console.error('Error loading digital vs retail:', error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) {
    return <div className="text-center py-8 text-gray-500">Loading...</div>;
  }

  if (!data) {
    return <div className="text-center py-8 text-gray-500">No data available</div>;
  }

  const chartData = [
    {
      type: 'Retail',
      orders: data.retail.orders,
      spending: data.retail.spending,
    },
    {
      type: 'Digital',
      orders: data.digital.orders,
      spending: data.digital.spending,
    },
  ];

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-gray-900">Digital vs Retail</h2>
        <div className="flex gap-2">
          <button
            onClick={() => setView('orders')}
            className={`px-4 py-2 rounded text-sm font-medium ${
              view === 'orders'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Orders
          </button>
          <button
            onClick={() => setView('spending')}
            className={`px-4 py-2 rounded text-sm font-medium ${
              view === 'spending'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Spending
          </button>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="type" tick={{ fontSize: 12 }} />
          <YAxis 
            tickFormatter={(value) => view === 'spending' 
              ? `$${value.toLocaleString()}`
              : value.toLocaleString()
            }
            tick={{ fontSize: 12 }}
          />
          <Tooltip 
            formatter={(value: number | undefined) => value ? (view === 'spending'
              ? `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
              : value.toLocaleString()) : ''
            }
          />
          <Legend />
          {view === 'orders' ? (
            <Bar dataKey="orders" fill="#3B82F6" name="Orders" />
          ) : (
            <Bar dataKey="spending" fill="#10B981" name="Spending" />
          )}
        </BarChart>
      </ResponsiveContainer>
      <div className="mt-4 grid grid-cols-2 gap-4">
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-sm font-medium text-gray-500 mb-1">Retail</h3>
          <p className="text-2xl font-bold text-gray-900">{data.retail.orders.toLocaleString()} orders</p>
          <p className="text-sm text-gray-600">
            ${data.retail.spending.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </p>
        </div>
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-sm font-medium text-gray-500 mb-1">Digital</h3>
          <p className="text-2xl font-bold text-gray-900">{data.digital.orders.toLocaleString()} orders</p>
          <p className="text-sm text-gray-600">
            ${data.digital.spending.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </p>
        </div>
      </div>
    </div>
  );
};

export default DigitalVsRetailChart;
