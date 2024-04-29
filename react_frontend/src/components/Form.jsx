import React from 'react';

const Form = () => {
    return (
        <div className='p-4'>
            <div className='max-w-[720px] m-auto'>
                <h1 className='font-bold text-4xl pb-4'>Opret prismatch</h1>
                <form className='my-8'>
                    <div className='mb-4'>
                        <label for='product_link' className='block mb-2 text-sm font-medium'>Produkt link (ikke til Coolshop)</label>
                        <input type='text' id='product_link' className='border hover:border-slate-400 focus:border-slate-400 focus:outline-none text-sm rounded block w-full p-2.5 bg-gray-200' placeholder='coolwebsite.com/coolproduct' required />
                    </div>
                    <div className='mb-4'>
                        <label for='product_link' className='block mb-2 text-sm font-medium'>Dit postnummer</label>
                        <input type='text' id='product_link' className='border hover:border-slate-400 focus:border-slate-400 focus:outline-none text-sm rounded block w-full p-2.5 bg-gray-200' placeholder='9400' required />
                    </div>
                    <div className='mb-4'>
                        <label for='product_link' className='block mb-2 text-sm font-medium'>Din email</label>
                        <input type='text' id='product_link' className='border hover:border-slate-400 focus:border-slate-400 focus:outline-none text-sm rounded block w-full p-2.5 bg-gray-200' placeholder='imcool@gmail.com' required />
                    </div>
                </form>
                <button className='focus:outline-none border focus:from-blue-600 focus:to-blue-900 rounded p-4 px-8 bg-gradient-to-b from-blue-500 to-blue-800 hover:from-blue-600 hover:to-blue-900 w-full text-white font-bold text-xl'>Indsend formular 🚀</button>
            </div>
        </div>
    )
}

export default Form
