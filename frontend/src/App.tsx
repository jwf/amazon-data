import React, { useState, useEffect } from 'react';
import { getSummary, SummaryStats } from './api';
import SummaryCard from './components/SummaryCard';
import SpendingOverTimeChart from './components/SpendingOverTimeChart';
import TopProductsChart from './components/TopProductsChart';
import CategoryBreakdown from './components/CategoryBreakdown';
import PaymentMethodsChart from './components/PaymentMethodsChart';
import ReturnStatsCard from './components/ReturnStatsCard';
import DigitalVsRetailChart from './components/DigitalVsRetailChart';
import RetailBreakdown from './components/RetailBreakdown';
import DigitalBreakdown from './components/DigitalBreakdown';

function App() {
  const [summary, setSummary] = useState<SummaryStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadSummary = async () => {
      try {
        const data = await getSummary();
        setSummary(data);
      } catch (error) {
        console.error('Error loading summary:', error);
      } finally {
        setLoading(false);
      }
    };
    loadSummary();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-xl text-gray-600">Loading your Amazon data...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Amazon Purchase Analytics</h1>
          <p className="mt-2 text-sm text-gray-600">
            Analyze your Amazon purchasing habits over time
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {summary && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <SummaryCard
              title="Total Spending"
              value={`$${summary.totalSpending.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
              subtitle={`${summary.totalOrders.toLocaleString()} orders`}
            />
            <SummaryCard
              title="Retail Orders"
              value={summary.totalRetailOrders.toLocaleString()}
              subtitle={`$${summary.totalRetailSpending.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
            />
            <SummaryCard
              title="Digital Orders"
              value={summary.totalDigitalOrders.toLocaleString()}
              subtitle={`$${summary.totalDigitalSpending.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
            />
            <SummaryCard
              title="Average Order Value"
              value={`$${summary.averageOrderValue.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
              subtitle={
                summary.dateRange.start && summary.dateRange.end
                  ? `${new Date(summary.dateRange.start).getFullYear()} - ${new Date(summary.dateRange.end).getFullYear()}`
                  : 'All time'
              }
            />
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <SpendingOverTimeChart />
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <DigitalVsRetailChart />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <CategoryBreakdown />
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <PaymentMethodsChart />
          </div>
        </div>

        <div className="grid grid-cols-1 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <TopProductsChart />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <ReturnStatsCard />
        </div>

        {/* Retail Breakdown Section */}
        <div className="mt-12 bg-gray-50 rounded-lg p-8">
          <RetailBreakdown />
        </div>

        {/* Digital Breakdown Section */}
        <div className="mt-12 bg-gray-50 rounded-lg p-8">
          <DigitalBreakdown />
        </div>
      </main>
    </div>
  );
}

export default App;
