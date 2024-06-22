export const fetchData = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/pricematches/');
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
};

export const updateItem = async (id,updatedItem) => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/pricematches/${id}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updatedItem),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    await response.text();
  } catch (error) {
    throw error;
  }
};
