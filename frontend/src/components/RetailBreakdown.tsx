import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { getRetailBreakdown, RetailBreakdown } from '../api';

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#06B6D4', '#84CC16'];

const RetailBreakdownComponent: React.FC = () => {
  const [data, setData] = useState<RetailBreakdown | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const result = await getRetailBreakdown();
        setData(result);
      } catch (error) {
        console.error('Error loading retail breakdown:', error);
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
      <h2 className="text-2xl font-bold text-gray-900">Retail Purchases Breakdown</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Categories */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Categories</h3>
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={categoryChartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {categoryChartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                formatter={(value: number | undefined, name?: string) => [
                  value ? `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` : '',
                  name || ''
                ]}
              />
              <Legend 
                wrapperStyle={{ paddingTop: '20px' }}
                iconType="circle"
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3 max-h-64 overflow-y-auto">
            {data.categories.slice(0, 10).map((cat, index) => {
              const total = data.categories.reduce((sum, c) => sum + c.spending, 0);
              const percent = total > 0 ? (cat.spending / total) * 100 : 0;
              return (
                <div key={cat.name} className="flex justify-between items-center bg-gray-50 p-2 rounded text-xs">
                  <div className="flex items-center flex-1 min-w-0">
                    <div 
                      className="w-3 h-3 rounded mr-2 flex-shrink-0" 
                      style={{ backgroundColor: COLORS[index % COLORS.length] }}
                    />
                    <span className="text-gray-900 font-medium truncate">{cat.name}</span>
                    <span className="text-gray-500 ml-2">{percent.toFixed(1)}%</span>
                  </div>
                  <span className="text-gray-900 font-semibold ml-2">
                    ${cat.spending.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
                  </span>
                </div>
              );
            })}
          </div>
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
                stroke="#3B82F6" 
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
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Retail Products</h3>
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
            <Bar dataKey="spending" fill="#10B981" name="Spending" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Payment Methods */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Payment Methods</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data.paymentMethods}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="method" 
              angle={-45}
              textAnchor="end"
              height={100}
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
            <Bar dataKey="spending" fill="#8B5CF6" name="Spending" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default RetailBreakdownComponent;
