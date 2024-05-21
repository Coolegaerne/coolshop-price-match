import React, { useState } from 'react';
import PriceMatchModal from './PriceMatchModal';

const PriceMatchTable = ({ data }) => {
  const [sortConfig, setSortConfig] = useState(null);
  const [selectedItem, setSelectedItem] = useState(null);

  const sortedData = [...data];
  if (sortConfig !== null) {
    sortedData.sort((a, b) => {
      if (a[sortConfig.key] < b[sortConfig.key]) {
        return sortConfig.direction === 'ascending' ? -1 : 1;
      }
      if (a[sortConfig.key] > b[sortConfig.key]) {
        return sortConfig.direction === 'ascending' ? 1 : -1;
      }
      return 0;
    });
  }

  const requestSort = key => {
    let direction = 'ascending';
    if (
      sortConfig &&
      sortConfig.key === key &&
      sortConfig.direction === 'ascending'
    ) {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  return (
    <div>
      <table className="min-w-full bg-white">
        <thead className="bg-gray-200">
          <tr>
            <th onClick={() => requestSort('creation_datetime')} className="cursor-pointer p-4 text-left">Creation Date</th>
            <th onClick={() => requestSort('url')} className="cursor-pointer p-4 text-left">URL</th>
            <th onClick={() => requestSort('accepted')} className="p-4 text-left">Status</th>
            <th className="p-4 text-left">See more</th>
          </tr>
        </thead>
        <tbody>
          {sortedData.map((item, index) => (
            <tr key={index} className={`border-t ${index % 2 === 1 ? 'bg-gray-100' : ''}`}>
              <td className="p-4">{item.creation_datetime}</td>
              <td className="p-4">{item.url}</td>
              <td className="p-4">{item.accepted ? 'Accepted' : 'Not Accepted'}</td>
              <td className="p-4">
                <button
                  onClick={() => setSelectedItem(item)}
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded center"
                >
                  Details
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {selectedItem && (
        <PriceMatchModal item={selectedItem} onClose={() => setSelectedItem(null)} />
      )}
    </div>
  );
};

export default PriceMatchTable;
