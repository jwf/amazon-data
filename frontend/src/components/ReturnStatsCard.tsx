import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { getReturns, ReturnStats } from '../api';

const ReturnStatsCard: React.FC = () => {
  const [stats, setStats] = useState<ReturnStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const result = await getReturns();
        setStats(result);
      } catch (error) {
        console.error('Error loading return stats:', error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) {
    return <div className="text-center py-8 text-gray-500">Loading...</div>;
  }

  if (!stats) {
    return <div className="text-center py-8 text-gray-500">No data available</div>;
  }

  const chartData = stats.returnsOverTime.labels.map((label, index) => ({
    period: label,
    returns: stats.returnsOverTime.values[index],
  }));

  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Return Statistics</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-sm font-medium text-gray-500 mb-1">Total Returns</h3>
          <p className="text-3xl font-bold text-gray-900">{stats.totalReturns}</p>
        </div>
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-sm font-medium text-gray-500 mb-1">Return Rate</h3>
          <p className="text-3xl font-bold text-gray-900">{stats.returnRate.toFixed(2)}%</p>
        </div>
      </div>
      {stats.returnsOverTime.labels.length > 0 && (
        <div>
          <h3 className="text-lg font-medium text-gray-700 mb-4">Returns Over Time</h3>
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
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="returns" 
                stroke="#EF4444" 
                strokeWidth={2}
                name="Returns"
                dot={{ r: 3 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
};

export default ReturnStatsCard;
