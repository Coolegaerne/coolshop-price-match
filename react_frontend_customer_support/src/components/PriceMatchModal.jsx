import React, { useState } from 'react';
import { CopyToClipboard } from 'react-copy-to-clipboard';

const PriceMatchModal = ({ item, onClose }) => {
    const [copyStatus, setCopyStatus] = useState({});
    const [editedItem, setEditedItem] = useState(item);

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

    const handleSaveAndClose = () => {
        onClose();
    };

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
    ];

    return (
        <div className="fixed inset-0 flex items-center bg-gray-600 bg-opacity-50 z-50">
            <div className="bg-white p-8 px-20 max-w-screen-xl mx-auto rounded shadow-lg">
                {fields.map((field, index) => (
                    <div className="mb-4 flex items-center justify-between" key={index}>
                        <label className="block mb-1 font-bold">{field.label}:&emsp;</label>

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
                    </div>
                ))}

                <hr className="my-4" />

                <div className="mb-4">
                    <label className="block mb-1 font-bold">Accepteret</label>
                    <div className="flex items-center space-x-2">
                        <button onClick={() => handleAcceptToggle(true)} className="p-2 bg-green-500 text-white rounded">✔️</button>
                        <button onClick={() => handleAcceptToggle(false)} className="p-2 bg-red-500 text-white rounded">❌</button>
                    </div>
                </div>

                <button onClick={handleSaveAndClose} className="mt-4 px-4 py-2 bg-blue-500 text-white rounded">
                    Close
                </button>
            </div>
        </div>
    );
};

export default PriceMatchModal;
