import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, Tooltip, ReferenceDot } from 'recharts';
import DateFilter from '../components/DateFilter';

export default function Dashboard() {
  const [data, setData] = useState([]);
  const [events, setEvents] = useState([]);
  const [start, setStart] = useState('2010-01-01');
  const [end, setEnd] = useState('2023-01-01');

  useEffect(() => {
    axios.get(`/api/data?start=${start}&end=${end}`).then(res => setData(res.data));
    axios.get(`/api/events`).then(res => setEvents(res.data));
  }, [start, end]);

  return (
    <div>
      <h2>📈 Brent Oil Price Dashboard</h2>
      <DateFilter start={start} end={end} setStart={setStart} setEnd={setEnd} />
      <LineChart width={1000} height={400} data={data}>
        <XAxis dataKey="Date" />
        <YAxis domain={['dataMin', 'dataMax']} />
        <Tooltip />
        <Line type="monotone" dataKey="Price" stroke="#8884d8" />
        {events.map((e, idx) => (
          <ReferenceDot key={idx} x={e.Date} y={e.Price} r={4} fill="red" />
        ))}
      </LineChart>
    </div>
  );
}
