export const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/pricematches/');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      throw error;
    }
  };
  
  export const updateItem = async (updatedItem) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/pricematches/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedItem),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const responseData = await response.text();
      console.log('Response:', responseData); // Log the response data
      return responseData; // Return plain text response
    } catch (error) {
      throw error;
    }
  };