import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { getCategories, Category } from '../api';

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#06B6D4', '#84CC16'];

const CategoryBreakdown: React.FC = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const result = await getCategories();
        setCategories(result.categories);
      } catch (error) {
        console.error('Error loading categories:', error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) {
    return <div className="text-center py-8 text-gray-500">Loading...</div>;
  }

  if (categories.length === 0) {
    return <div className="text-center py-8 text-gray-500">No data available</div>;
  }

  const chartData = categories.map(cat => ({
    name: cat.name,
    value: cat.spending,
  }));

  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Spending by Category</h2>
      <ResponsiveContainer width="100%" height={400}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip 
            formatter={(value: number | undefined) => value ? `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` : ''}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
        {categories.map((cat, index) => {
          const total = categories.reduce((sum, c) => sum + c.spending, 0);
          const percent = total > 0 ? (cat.spending / total) * 100 : 0;
          return (
            <div key={cat.name} className="flex justify-between items-center bg-gray-50 p-3 rounded">
              <div className="flex items-center flex-1">
                <div 
                  className="w-4 h-4 rounded mr-3 flex-shrink-0" 
                  style={{ backgroundColor: COLORS[index % COLORS.length] }}
                />
                <div className="flex-1 min-w-0">
                  <span className="text-sm font-medium text-gray-900 block truncate">{cat.name}</span>
                  <span className="text-xs text-gray-500">{percent.toFixed(1)}%</span>
                </div>
              </div>
              <span className="text-sm font-semibold text-gray-900 ml-4">
                ${cat.spending.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default CategoryBreakdown;
