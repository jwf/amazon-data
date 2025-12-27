import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { getTopProducts, TopProduct } from '../api';

const TopProductsChart: React.FC = () => {
  const [products, setProducts] = useState<TopProduct[]>([]);
  const [by, setBy] = useState<'quantity' | 'spending'>('quantity');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const result = await getTopProducts(15, by);
        setProducts(result.products);
      } catch (error) {
        console.error('Error loading top products:', error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [by]);

  if (loading) {
    return <div className="text-center py-8 text-gray-500">Loading...</div>;
  }

  if (products.length === 0) {
    return <div className="text-center py-8 text-gray-500">No data available</div>;
  }

  const chartData = products.map(product => ({
    name: product.name.length > 50 ? product.name.substring(0, 50) + '...' : product.name,
    fullName: product.name,
    quantity: product.quantity,
    spending: product.spending,
  }));

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-gray-900">Top Products</h2>
        <div className="flex gap-2">
          <button
            onClick={() => setBy('quantity')}
            className={`px-4 py-2 rounded text-sm font-medium ${
              by === 'quantity'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            By Quantity
          </button>
          <button
            onClick={() => setBy('spending')}
            className={`px-4 py-2 rounded text-sm font-medium ${
              by === 'spending'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            By Spending
          </button>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={500}>
        <BarChart data={chartData} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" tick={{ fontSize: 12 }} />
          <YAxis 
            dataKey="name" 
            type="category" 
            width={300}
            tick={{ fontSize: 10 }}
          />
          <Tooltip 
            formatter={(value: number | undefined) => value ? (by === 'spending' 
              ? `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
              : value.toLocaleString()) : ''
            }
            contentStyle={{ maxWidth: 400 }}
          />
          <Legend />
          {by === 'quantity' ? (
            <Bar dataKey="quantity" fill="#3B82F6" name="Quantity" />
          ) : (
            <Bar dataKey="spending" fill="#10B981" name="Spending" />
          )}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TopProductsChart;
