import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';
import axios from 'axios';
import { useEffect, useState } from 'react';

export default function PriceChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/api/prices').then(res => {
      setData(res.data);
    });
  }, []);

  return (
    <div className="chart-container">
      <h2>Brent Oil Log Returns</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid stroke="#ccc" />
          <XAxis dataKey="Date" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="LogReturn" stroke="#007BFF" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
