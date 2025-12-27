import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { getSpendingOverTime, SpendingOverTime } from '../api';

const SpendingOverTimeChart: React.FC = () => {
  const [data, setData] = useState<SpendingOverTime | null>(null);
  const [period, setPeriod] = useState<'monthly' | 'yearly'>('monthly');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const result = await getSpendingOverTime(period);
        setData(result);
      } catch (error) {
        console.error('Error loading spending over time:', error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [period]);

  if (loading) {
    return <div className="text-center py-8 text-gray-500">Loading...</div>;
  }

  if (!data || data.labels.length === 0) {
    return <div className="text-center py-8 text-gray-500">No data available</div>;
  }

  const chartData = data.labels.map((label, index) => ({
    period: label,
    spending: data.values[index],
    orders: data.orderCounts[index],
  }));

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-gray-900">Spending Over Time</h2>
        <div className="flex gap-2">
          <button
            onClick={() => setPeriod('monthly')}
            className={`px-4 py-2 rounded text-sm font-medium ${
              period === 'monthly'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Monthly
          </button>
          <button
            onClick={() => setPeriod('yearly')}
            className={`px-4 py-2 rounded text-sm font-medium ${
              period === 'yearly'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Yearly
          </button>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="period" 
            angle={-45}
            textAnchor="end"
            height={80}
            tick={{ fontSize: 12 }}
          />
          <YAxis 
            tickFormatter={(value) => `$${value.toLocaleString()}`}
            tick={{ fontSize: 12 }}
          />
          <Tooltip 
            formatter={(value: number | undefined) => value ? `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` : ''}
          />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="spending" 
            stroke="#3B82F6" 
            strokeWidth={2}
            name="Spending"
            dot={{ r: 3 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SpendingOverTimeChart;
