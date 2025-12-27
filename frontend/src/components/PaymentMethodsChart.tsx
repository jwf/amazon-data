import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { getPaymentMethods, PaymentMethod } from '../api';

const PaymentMethodsChart: React.FC = () => {
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethod[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const result = await getPaymentMethods();
        setPaymentMethods(result.paymentMethods);
      } catch (error) {
        console.error('Error loading payment methods:', error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) {
    return <div className="text-center py-8 text-gray-500">Loading...</div>;
  }

  if (paymentMethods.length === 0) {
    return <div className="text-center py-8 text-gray-500">No data available</div>;
  }

  const chartData = paymentMethods.map(pm => ({
    method: pm.method,
    spending: pm.spending,
  }));

  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Spending by Payment Method</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
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
  );
};

export default PaymentMethodsChart;
