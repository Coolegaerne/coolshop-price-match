import React, { useState, useEffect  } from 'react';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { updateItem } from '../utils';

const PriceMatchModal = ({ item, onClose, onSave }) => {
  const [copyStatus, setCopyStatus] = useState({});
  const [editedItem, setEditedItem] = useState(item);

  useEffect(() => {
    const handleEsc = (event) => {
      if (event.key === 'Escape') {
        handleCloseWithoutSave();
      }
    };

    document.addEventListener('keydown', handleEsc);

    return () => {
      document.removeEventListener('keydown', handleEsc);
    };
  }, []);

  const handleCopy = (field) => {
    setCopyStatus({ ...copyStatus, [field]: true });
    setTimeout(() => setCopyStatus({ ...copyStatus, [field]: false }), 2000);
  };

  const handleFieldChange = (field, value) => {
    setEditedItem({ ...editedItem, [field]: value });
  };

  const handleAcceptToggle = (value) => {
    setEditedItem({ ...editedItem, accepted: value });
  };

  const handleSaveAndClose = async () => {
    try {
      const updatedItem = { ...item, ...editedItem };
      const id = item.id;
      await updateItem(id, updatedItem);
      onSave(updatedItem);
      onClose();
    } catch (error) {
      console.error('Failed to update item:', error);
    }
  };

  const handleCloseWithoutSave = async () => {
    try {
      onClose();
    }
    catch (error) {
      console.error('Failed to close modal:', error);
    }
  }

  const openProductPageImage = async (productPage) => {
    try {
      var string = (`data:image/png;base64,${productPage}`);
      var iframe = "<iframe width='100%' height='100%' src='" + string + "'></iframe>"
      var image = window.open();
      image.document.open();
      image.document.write(iframe);
      image.document.close();
    }
    catch (error) {
      console.error('Failed to open product page image:', error);
    }
  }

  const fields = [
    { label: 'Navn', key: 'name' },
    { label: 'Url', key: 'url' },
    { label: 'EAN', key: 'ean' },
    { label: 'Lagerstatus', key: 'stock_status' },
    { label: 'Oprettelsesdato', key: 'creation_datetime' },
    { label: 'Pris', key: 'price' },
    { label: 'Fragtpris', key: 'shipping_price' },
    { label: 'Totalpris', key: 'total_price' },
    { label: 'Accepteret', key: 'accepted' },
    { label: 'Accepteringsdato', key: 'acceptance_datetime' },
    { label: 'Postnummer', key: 'postal_code' },
    { label: 'Email', key: 'email' },
    { label: 'Product page', key: 'product_image'},
  ];

  return (
    <div className="fixed inset-0 flex items-center bg-gray-600 bg-opacity-50 z-50">
      <div className="bg-white p-8 px-20 max-w-screen-xl mx-auto rounded shadow-lg max-h-screen overflow-y-scroll">
        {fields.map((field, index) => (
          <div className="mb-4 flex items-center justify-between" key={index}>
            <label className="block mb-1 font-bold">{field.label}:&emsp;</label>

            {field.label === 'Product page' ? (
              <img src={`data:image/png;base64,${editedItem[field.key]}`} alt="" />,
              <button onClick={() => openProductPageImage(editedItem[field.key])} className="mt-4 px-4 py-2 bg-blue-500 hover:bg-blue-600 active:bg-blue-400 text-white rounded">
                View product page
              </button>
            ) : (
              <div className="flex items-center">
                <input
                  type="text"
                  value={editedItem[field.key]}
                  onChange={(e) => handleFieldChange(field.key, e.target.value)}
                  className="flex-1 p-2 border border-gray-300 rounded min-w-0"
                />

                <CopyToClipboard text={editedItem[field.key]} onCopy={() => handleCopy(field.label)}>
                  <button className="p-2 mr-2 bg-gray-200 rounded">📄</button>
                </CopyToClipboard>

                {copyStatus[field.label] && <span className="ml-2 text-green-500">Copied!</span>}
              </div>
            )}
          </div>
        ))}

        <hr className="my-4" />
        <label className="block mb-1 font-bold">Accepter</label>
        <div className="flex gap-2">
          <button onClick={() => handleAcceptToggle(true)} className="p-2 bg-green-500 text-white rounded hover:bg-green-600 active:bg-green-400 w-full">Accept</button>
          <button onClick={() => handleAcceptToggle(false)} className="p-2 bg-red-500 text-white rounded hover:bg-red-600 active:bg-red-400 w-full">Deny</button>
        </div>

        <hr className="my-4" />
        <div className='flex gap-2'>
          <button onClick={handleSaveAndClose} className="mt-4 px-4 py-2 bg-blue-500 hover:bg-blue-600 active:bg-blue-400 text-white rounded w-full">Save and Close</button>
          <button onClick={handleCloseWithoutSave} className="mt-4 px-4 py-2 bg-blue-500 hover:bg-blue-600 active:bg-blue-400 text-white rounded w-full">Exit without saving</button>
        </div>
      </div>
    </div>
  );
};

export default PriceMatchModal;
