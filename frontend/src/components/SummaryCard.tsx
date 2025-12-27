import React from 'react';

interface SummaryCardProps {
  title: string;
  value: string;
  subtitle: string;
}

const SummaryCard: React.FC<SummaryCardProps> = ({ title, value, subtitle }) => {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-sm font-medium text-gray-500 mb-1">{title}</h3>
      <p className="text-3xl font-bold text-gray-900 mb-2">{value}</p>
      <p className="text-sm text-gray-600">{subtitle}</p>
    </div>
  );
};

export default SummaryCard;
