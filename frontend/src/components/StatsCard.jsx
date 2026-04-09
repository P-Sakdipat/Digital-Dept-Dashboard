import React from 'react';

export default function StatsCard({ title, value, valueClass = "text-gray-800" }) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col justify-center">
      <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wider">{title}</h3>
      <p className={`text-2xl font-bold mt-2 ${valueClass}`}>{value}</p>
    </div>
  );
}
