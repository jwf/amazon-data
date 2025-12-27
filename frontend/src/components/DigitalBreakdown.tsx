import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { getDigitalBreakdown, DigitalBreakdown } from '../api';

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#06B6D4', '#84CC16'];

const DigitalBreakdownComponent: React.FC = () => {
  const [data, setData] = useState<DigitalBreakdown | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const result = await getDigitalBreakdown();
        setData(result);
      } catch (error) {
        console.error('Error loading digital breakdown:', error);
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

  const categoryChartData = data.categories.map(cat => ({
    name: cat.name,
    value: cat.spending,
  }));

  const spendingChartData = data.spendingOverTime.labels.map((label, index) => ({
    period: label,
    spending: data.spendingOverTime.values[index],
  }));

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">Digital Purchases Breakdown</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Categories */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Digital Categories</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categoryChartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${((percent || 0) * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {categoryChartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                formatter={(value: number | undefined) => value ? `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` : ''}
              />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Spending Over Time */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Spending Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={spendingChartData}>
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
                stroke="#10B981" 
                strokeWidth={2}
                name="Spending"
                dot={{ r: 3 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Top Products */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Digital Products</h3>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={data.topProducts.slice(0, 10)} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" tick={{ fontSize: 12 }} />
            <YAxis 
              dataKey="name" 
              type="category" 
              width={300}
              tick={{ fontSize: 10 }}
            />
            <Tooltip 
              formatter={(value: number | undefined) => value ? `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` : ''}
              contentStyle={{ maxWidth: 400 }}
            />
            <Legend />
            <Bar dataKey="spending" fill="#3B82F6" name="Spending" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Subscriptions */}
      {data.subscriptions.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Subscriptions</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Purchases</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total Spending</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {data.subscriptions.map((sub, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{sub.name}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{sub.count}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">
                      ${sub.spending.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default DigitalBreakdownComponent;
