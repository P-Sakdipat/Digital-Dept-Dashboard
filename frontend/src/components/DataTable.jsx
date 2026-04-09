import React, { useState } from 'react';
import axios from 'axios';
import { Pencil, Trash2, Plus, X, Check } from 'lucide-react';

const API_ROOT = 'http://localhost:8000/api';

export default function DataTable({ data, total, page, setPage, searchTerm, setSearchTerm, isAdmin, refreshData }) {
  const [editingRow, setEditingRow] = useState(null);
  const [editFormData, setEditFormData] = useState({});
  const [isAdding, setIsAdding] = useState(false);
  
  const handleEditClick = (row) => {
    setEditingRow(row);
    setEditFormData({ ...row });
  };

  const handleCancelEdit = () => {
    setEditingRow(null);
    setEditFormData({});
    setIsAdding(false);
  };

  const handleSaveEdit = async () => {
    try {
      if (isAdding) {
        await axios.post(`${API_ROOT}/sales/`, editFormData);
      } else {
        await axios.put(`${API_ROOT}/sales/${editFormData.VBELN}/${editFormData.POSNR}/`, editFormData);
      }
      setEditingRow(null);
      setIsAdding(false);
      refreshData();
    } catch (e) {
      console.error("Error saving data", e);
      alert("Failed to save data.");
    }
  };

  const handleDelete = async (row) => {
    if (window.confirm("Are you sure you want to delete this record?")) {
      try {
        await axios.delete(`${API_ROOT}/sales/${row.VBELN}/${row.POSNR}/`);
        refreshData();
      } catch (e) {
        console.error("Error deleting data", e);
        alert("Failed to delete.");
      }
    }
  };

  const handleAddClick = () => {
    setIsAdding(true);
    setEditingRow({ VBELN: '', POSNR: '' }); // dummy
    setEditFormData({ VBELN: '', POSNR: '', NetValue: 0, Quantity: 0, ARKTX: '', SoldToName1: '' });
  };

  const handleFormChange = (e, field) => {
    setEditFormData({ ...editFormData, [field]: e.target.value });
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-700">Sales Records</h3>
        <div className="flex items-center gap-3">
          <input
            type="text"
            placeholder="Search by Product Name..."
            className="border border-gray-300 rounded-md px-3 py-1.5 text-sm w-64 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          {isAdmin && (
            <button 
              onClick={handleAddClick}
              className="bg-indigo-600 text-white px-3 py-1.5 rounded-md text-sm flex items-center gap-1 hover:bg-indigo-700 transition"
            >
              <Plus className="w-4 h-4" /> Add New
            </button>
          )}
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 text-sm text-left">
          <thead className="bg-gray-50 text-gray-500 uppercase">
            <tr>
              <th className="px-4 py-3">Date</th>
              <th className="px-4 py-3">Doc #</th>
              <th className="px-4 py-3">Item #</th>
              <th className="px-4 py-3">Product</th>
              <th className="px-4 py-3">Customer</th>
              <th className="px-4 py-3 text-right">Quantity</th>
              <th className="px-4 py-3 text-right">Net Value</th>
              {isAdmin && <th className="px-4 py-3 text-center">Actions</th>}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {isAdding && (
               <tr className="bg-indigo-50">
                   <td className="px-4 py-2"><input type="text" className="w-full border p-1" placeholder="Date" value={editFormData.FKDAT || ''} onChange={(e) => handleFormChange(e, 'FKDAT')} /></td>
                   <td className="px-4 py-2"><input type="text" className="w-full border p-1" placeholder="VBELN" value={editFormData.VBELN || ''} onChange={(e) => handleFormChange(e, 'VBELN')} /></td>
                   <td className="px-4 py-2"><input type="text" className="w-full border p-1" placeholder="POSNR" value={editFormData.POSNR || ''} onChange={(e) => handleFormChange(e, 'POSNR')} /></td>
                   <td className="px-4 py-2"><input type="text" className="w-full border p-1" placeholder="Product" value={editFormData.ARKTX || ''} onChange={(e) => handleFormChange(e, 'ARKTX')} /></td>
                   <td className="px-4 py-2"><input type="text" className="w-full border p-1" placeholder="Customer" value={editFormData.SoldToName1 || ''} onChange={(e) => handleFormChange(e, 'SoldToName1')} /></td>
                   <td className="px-4 py-2"><input type="number" className="w-full border p-1 text-right" value={editFormData.Quantity || 0} onChange={(e) => handleFormChange(e, 'Quantity')} /></td>
                   <td className="px-4 py-2"><input type="number" step="0.01" className="w-full border p-1 text-right" value={editFormData.NetValue || 0} onChange={(e) => handleFormChange(e, 'NetValue')} /></td>
                   <td className="px-4 py-2 flex justify-center gap-2">
                       <button onClick={handleSaveEdit} className="text-green-600 hover:text-green-800"><Check className="w-4 h-4"/></button>
                       <button onClick={handleCancelEdit} className="text-red-500 hover:text-red-700"><X className="w-4 h-4"/></button>
                   </td>
               </tr>
            )}
            {data.map((row, idx) => {
              const isEditing = editingRow && editingRow.VBELN === row.VBELN && editingRow.POSNR === row.POSNR && !isAdding;
              return (
                <tr key={`${row.VBELN}-${row.POSNR}-${idx}`} className="hover:bg-gray-50 transition-colors">
                  <td className="px-4 py-3">{row.FKDAT}</td>
                  <td className="px-4 py-3">{row.VBELN}</td>
                  <td className="px-4 py-3">{row.POSNR}</td>
                  <td className="px-4 py-3 text-gray-700">
                     {isEditing ? <input type="text" className="border p-1 w-full" value={editFormData.ARKTX} onChange={(e) => handleFormChange(e, 'ARKTX')} /> : row.ARKTX}
                  </td>
                  <td className="px-4 py-3">
                     {isEditing ? <input type="text" className="border p-1 w-full" value={editFormData.SoldToName1} onChange={(e) => handleFormChange(e, 'SoldToName1')} /> : row.SoldToName1}
                  </td>
                  <td className="px-4 py-3 text-right">
                     {isEditing ? <input type="number" className="border p-1 w-full text-right" value={editFormData.Quantity} onChange={(e) => handleFormChange(e, 'Quantity')} /> : row.Quantity?.toLocaleString()}
                  </td>
                  <td className="px-4 py-3 text-right font-medium">
                     {isEditing ? <input type="number" step="0.01" className="border p-1 w-full text-right" value={editFormData.NetValue} onChange={(e) => handleFormChange(e, 'NetValue')} /> : `฿${row.NetValue?.toLocaleString()}`}
                  </td>
                  {isAdmin && (
                    <td className="px-4 py-3 text-center">
                      {isEditing ? (
                         <div className="flex justify-center gap-2">
                            <button onClick={handleSaveEdit} className="text-green-600 hover:text-green-800"><Check className="w-4 h-4"/></button>
                            <button onClick={handleCancelEdit} className="text-red-500 hover:text-red-700"><X className="w-4 h-4"/></button>
                         </div>
                      ) : (
                         <div className="flex justify-center gap-3">
                            <button onClick={() => handleEditClick(row)} className="text-indigo-500 hover:text-indigo-700"><Pencil className="w-4 h-4"/></button>
                            <button onClick={() => handleDelete(row)} className="text-red-500 hover:text-red-700"><Trash2 className="w-4 h-4"/></button>
                         </div>
                      )}
                    </td>
                  )}
                </tr>
              )
            })}
          </tbody>
        </table>
        {data.length === 0 && <div className="text-center py-8 text-gray-500">No records found</div>}
      </div>

      <div className="flex justify-between items-center mt-4">
          <div className="text-sm text-gray-500">
             Showing {(page - 1) * 10 + 1} to {Math.min(page * 10, total)} of {total} entries
          </div>
          <div className="flex gap-2">
             <button 
                onClick={() => setPage(Math.max(1, page - 1))} 
                disabled={page === 1}
                className="px-3 py-1 border rounded text-sm disabled:opacity-50"
             >
                 Prev
             </button>
             <button 
                onClick={() => setPage(page + 1)} 
                disabled={page * 10 >= total}
                className="px-3 py-1 border rounded text-sm disabled:opacity-50"
             >
                 Next
             </button>
          </div>
      </div>
    </div>
  );
}
