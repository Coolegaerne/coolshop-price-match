import React from 'react';
import { useLocation } from 'react-router-dom';

const AlreadyExist = () => {
    const searchParams = new URLSearchParams(useLocation().search);
    const message = searchParams.get('message');

    return (
        <div className="p-4">
            <h2 className="text-2xl font-bold">Already Exist</h2>
            <p>{message}</p>
        </div>
    );
}

export default AlreadyExist;
