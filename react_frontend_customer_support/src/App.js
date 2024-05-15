import React, { useState, useEffect } from 'react';
import PriceMatchTable from './components/PriceMatchTable';
import './index.css';

const mockData = [
  { 
    name: 'Product 1',
    url: 'https://example.com/product1',
    price: '100',
    ean: '1234567890123',
    shipping_price: '10',
    stock_status: 'In Stock',
    total_price: 110,
    accepted: true,
    creation_datetime: '2024-05-01',
    acceptance_datetime: '2024-05-02',
    product_image: '', // You can add image data here if needed
    postal_code: '12345',
    email: 'example@example.com'
  },
  { 
    name: 'Product 2',
    url: 'https://example.com/product2',
    price: '150',
    ean: '9876543210987',
    shipping_price: '15',
    stock_status: 'Out of Stock',
    total_price: 165,
    accepted: false,  
    creation_datetime: '2024-05-03',
    acceptance_datetime: null,
    product_image: '', // You can add image data here if needed
    postal_code: '54321',
    email: 'another@example.com'
  },
  // Add more mock data if needed
];

function App() {
  const [data, setData] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    // Fetch data from API
    // Simulating with mock data here
    setData(mockData);
  }, []);

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
      <PriceMatchTable data={filteredData} />
    </div>
  );
}

export default App;
