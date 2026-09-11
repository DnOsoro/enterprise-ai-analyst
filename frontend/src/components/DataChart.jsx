import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

export default function DataChart({ data }) {
  if (!data || data.length === 0) return null;

  const keys = Object.keys(data[0]);
  const xAxisKey = keys[0];
  const dataKey = keys[1] || keys[0];

  return (
    <div className="w-full h-72 bg-[#161b2a] p-4 rounded-xl border border-[#23293e]">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#23293e" vertical={false} />
          <XAxis dataKey={xAxisKey} stroke="#94a3b8" fontSize={12} tickLine={false} />
          <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#111521', borderColor: '#23293e', color: '#f8fafc', borderRadius: '8px' }} 
            itemStyle={{ color: '#818cf8' }}
          />
          <Bar dataKey={dataKey} fill="#6366f1" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}