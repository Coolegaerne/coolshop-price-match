import React, { useState } from 'react';

const Form = () => {
    const [formData, setFormData] = useState({
        url: '',
        email: '',
        postal_code: ''
    });
    const [buttonDisabled, setButtonDisabled] = useState(false);

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setButtonDisabled(true);

        try {
            const response = await fetch('http://127.0.0.1:8000/scrape/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                let response_data = await response.json();
                switch(response_data.message) {
                    case 'SUCCESS':
                        window.location.href = "/success";
                        break;
                    case 'ALREADY_EXIST':

                        window.location.href = `/already_exist?message=${response_data.message}`;
                        break;
                    default:
                        window.location.href = "/error";
                }
            } else {
                window.location.href = "/error";
            }
        } catch (error) {
            window.location.href = "/error";
        } finally {
            setButtonDisabled(false);
        }
    };

    return (
        <div className='p-4'>
            <div className='max-w-[720px] m-auto'>
                <h1 className='font-bold text-4xl pb-4'>Opret prismatch</h1>
                <form className='my-8' onSubmit={handleSubmit}>
                    <div className='mb-4'>
                        <label htmlFor='url' className='block mb-2 text-sm font-medium'>Produkt link (ikke til Coolshop)</label>
                        <input type='text' id='url' name='url' value={formData.url} onChange={handleChange} className='border hover:border-slate-400 focus:border-slate-400 focus:outline-none text-sm rounded block w-full p-2.5 bg-gray-200' placeholder='coolwebsite.com/coolproduct' required />
                    </div>
                    <div className='mb-4'>
                        <label htmlFor='postal_code' className='block mb-2 text-sm font-medium'>Dit postnummer</label>
                        <input type='text' id='postal_code' name='postal_code' value={formData.postal_code} onChange={handleChange} className='border hover:border-slate-400 focus:border-slate-400 focus:outline-none text-sm rounded block w-full p-2.5 bg-gray-200' placeholder='9400' required />
                    </div>
                    <div className='mb-4'>
                        <label htmlFor='email' className='block mb-2 text-sm font-medium'>Din email</label>
                        <input type='email' id='email' name='email' value={formData.email} onChange={handleChange} className='border hover:border-slate-400 focus:border-slate-400 focus:outline-none text-sm rounded block w-full p-2.5 bg-gray-200' placeholder='imcool@gmail.com' required />
                    </div>
                    <button type='submit' disabled={buttonDisabled} className='focus:outline-none border focus:from-blue-600 focus:to-blue-900 rounded p-4 px-8 bg-gradient-to-b from-blue-500 to-blue-800 hover:from-blue-600 hover:to-blue-900 w-full text-white font-bold text-xl'>Indsend formular 🚀</button>
                </form>
            </div>
        </div>
    );
}

export default Form;
