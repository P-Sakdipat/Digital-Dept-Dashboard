import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { ShieldAlert, ShieldCheck } from 'lucide-react';
import { PieChart, Pie, Cell, Tooltip as RechartsTooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';

import StatsCard from './components/StatsCard';
import DataTable from './components/DataTable';

const API_ROOT = import.meta.env.DEV ? 'http://localhost:8000/api' : '/_/backend/api';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#ffc658'];

const formatToMillion = (value) => {
  if (value === undefined || value === null) return "0.00";
  if (Math.abs(value) >= 1000000) {
    return (value / 1000000).toFixed(2) + 'M';
  }
  return value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
};

export default function Dashboard() {
  const [isAdmin, setIsAdmin] = useState(false);
  const [summary, setSummary] = useState(null);
  const [salesData, setSalesData] = useState([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  // Filter states
  const [searchTerm, setSearchTerm] = useState('');
  const [timeFilter, setTimeFilter] = useState('all');
  const [refDate, setRefDate] = useState('');

  const fetchSummary = async () => {
    try {
      const { data } = await axios.get(`${API_ROOT}/summary/?time_filter=${timeFilter}&ref_date=${refDate}`);
      setSummary(data);
    } catch (e) {
      console.error('Error fetching summary:', e);
    }
  };

  const fetchSalesData = async () => {
    try {
      let url = `${API_ROOT}/sales/?page=${page}&page_size=10`;
      if (searchTerm) {
        url += `&ARKTX=${searchTerm}`; // Assuming search by material description, we can update backend to support ARKTX filtering if needed
      }
      const { data } = await axios.get(url);
      setSalesData(data.data);
      setTotal(data.total);
    } catch (e) {
      console.error('Error fetching sales data:', e);
    }
  };

  useEffect(() => {
    fetchSummary();
  }, [timeFilter, refDate]);

  useEffect(() => {
    fetchSalesData();
  }, [page, searchTerm]);

  const handleAdminToggle = () => {
    if (isAdmin) {
      setIsAdmin(false);
    } else {
      const pwd = window.prompt("Enter Admin Password:");
      if (pwd === 'admin123') {
        setIsAdmin(true);
      } else if (pwd !== null) {
        alert("Incorrect Password!");
      }
    }
  };

  if (!summary) return <div className="text-center w-full mt-20 text-gray-500">Loading data...</div>;

  return (
    <div className="w-full max-w-7xl mx-auto flex flex-col gap-6 w-full h-full">
      {/* Header */}
      <header className="flex justify-between items-center py-4 border-b border-gray-200">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Sales Analytics Dashboard</h1>
          <p className="text-sm text-gray-500">Overview of DSI Sales Dictionary</p>
        </div>
        <div className="flex items-center gap-4">
          <input
            type="date"
            value={refDate}
            onChange={(e) => setRefDate(e.target.value)}
            className="border border-gray-300 bg-white rounded-md px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm"
          />
          <select
            value={timeFilter}
            onChange={(e) => setTimeFilter(e.target.value)}
            className="border border-gray-300 bg-white rounded-md px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm"
          >
            <option value="all">All Time</option>
            <option value="year">Yearly</option>
            <option value="month">Monthly</option>
            <option value="week">Weekly</option>
            <option value="day">Daily</option>
          </select>
          <div className="border-l h-6 border-gray-300"></div>
          <span className="text-sm font-medium text-gray-600">
            {isAdmin ? 'Admin Mode On' : 'User Mode'}
          </span>
          <button
            onClick={handleAdminToggle}
            className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none ${isAdmin ? 'bg-indigo-600' : 'bg-gray-200'}`}
          >
            <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${isAdmin ? 'translate-x-6' : 'translate-x-1'}`} />
          </button>
          {isAdmin ? <ShieldCheck className="w-6 h-6 text-indigo-600" /> : <ShieldAlert className="w-6 h-6 text-gray-400" />}
        </div>
      </header>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-6 gap-4">
        <StatsCard title="Gross Sales" value={`฿${formatToMillion(summary.gross_sales)}`} />
        <StatsCard title="Returns / Adj" value={`฿${formatToMillion(summary.total_returns)}`} valueClass="text-red-500" />
        <StatsCard title="Net Revenue" value={`฿${formatToMillion(summary.total_sales)}`} />
        <StatsCard title="Total LC Value" value={`฿${formatToMillion(summary.total_lc_value)}`} />
        <StatsCard title="Total Quantity" value={formatToMillion(summary.total_quantity)} />
        <StatsCard title="Total Orders" value={summary.total_orders.toLocaleString()} />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex flex-col">
          <h3 className="text-lg font-semibold mb-4 text-gray-700">Sales by Material Group</h3>
          <div className="flex-1 min-h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={summary.sales_by_group}
                  dataKey="NetValue"
                  nameKey="MatGrDes"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  fill="#8884d8"
                  label={({ value }) => formatToMillion(value)}
                >
                  {summary.sales_by_group.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <RechartsTooltip formatter={(value) => `฿${formatToMillion(value)}`} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex flex-col">
          <h3 className="text-lg font-semibold mb-4 text-gray-700">Top 5 Customers</h3>
          <div className="flex-1 min-h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={summary.top_customers} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" tickFormatter={(value) => formatToMillion(value)} />
                <YAxis dataKey="SoldToName1" type="category" width={100} tick={{ fontSize: 10 }} />
                <RechartsTooltip formatter={(value) => `฿${formatToMillion(value)}`} />
                <Bar dataKey="NetValue" fill="#82ca9d" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Data Table */}
      <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 mb-10 overflow-hidden">
        <DataTable
          data={salesData}
          total={total}
          page={page}
          setPage={setPage}
          searchTerm={searchTerm}
          setSearchTerm={setSearchTerm}
          isAdmin={isAdmin}
          refreshData={() => { fetchSalesData(); fetchSummary(); }}
        />
      </div>
    </div>
  );
}
