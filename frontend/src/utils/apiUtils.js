/**
 * Format error messages from API responses
 * @param {Error} error - Axios error object
 * @returns {string} Formatted error message
 */
export const formatApiError = (error) => {
  // Check if the error has a response from the server
  if (error.response) {
    // The server responded with a status code outside the 2xx range
    const data = error.response.data;
    
    // Handle different response structures
    if (data.detail) {
      return data.detail;
    } else if (data.message) {
      return data.message;
    } else if (typeof data === 'string') {
      return data;
    } else if (Array.isArray(data)) {
      return data.map(item => item.message || item).join(', ');
    } else if (typeof data === 'object') {
      return Object.values(data).flat().join(', ');
    }
    
    return `Error: ${error.response.status} ${error.response.statusText}`;
  } else if (error.request) {
    // The request was made but no response was received
    return 'Network error. Please check your connection and try again.';
  } else {
    // Something else happened in setting up the request
    return error.message || 'An unexpected error occurred. Please try again.';
  }
};

/**
 * Handle API errors in a consistent way
 * @param {Error} error - Axios error object
 * @param {Function} setError - State setter for error message
 * @param {Function} setLoading - State setter for loading state
 */
export const handleApiError = (error, setError, setLoading = null) => {
  const errorMessage = formatApiError(error);
  setError(errorMessage);
  
  if (setLoading) {
    setLoading(false);
  }
  
  // Log the error for debugging
  console.error('API Error:', error);
};
