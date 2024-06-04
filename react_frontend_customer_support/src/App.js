import React, { useState, useEffect } from 'react';
import PriceMatchTable from './components/PriceMatchTable';
import './index.css';
import { fetchData } from './utils';

function App() {
  const [data, setData] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const getData = async () => {
      const result = await fetchData();
      setData(result);
    };
    getData();
  }, []);

  const handleSave = (updatedItem) => {
    setData(prevData => {
      return prevData.map(item => item.id === updatedItem.id ? updatedItem : item);
    });
  };

  const filteredData = data.filter(item =>
    Object.entries(item).some(([key, value]) => {
      if (key === 'creation_datetime' || key === 'url') {
        return value.toLowerCase().includes(searchTerm.toLowerCase());
      }
      return false;
    })
  );

  return (
    <div className="container mx-auto p-4">
      <input
        type="text"
        placeholder="Search"
        className="mb-4 p-2 border rounded w-full"
        value={searchTerm}
        onChange={e => setSearchTerm(e.target.value)}
      />
      <PriceMatchTable data={filteredData} onSave={handleSave} />
    </div>
  );
}

export default App;
