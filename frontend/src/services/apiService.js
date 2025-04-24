const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

/**
 * Service for interacting with the Web Research Agent API
 */
const apiService = {
  /**
   * Perform research based on a query
   * @param {string} query - The research query
   * @returns {Promise} - Promise resolving to research results
   */
  performResearch: async (query) => {
    try {
      const response = await fetch(`${API_BASE_URL}/research`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to perform research');
      }
      
      return await response.json();
    } catch (error) {
      console.error('API Service Error:', error);
      throw error;
    }
  },
  
  /**
   * Perform a web search
   * @param {string} query - The search query
   * @param {number} numResults - Number of results to return
   * @returns {Promise} - Promise resolving to search results
   */
  performSearch: async (query, numResults = 10) => {
    try {
      const response = await fetch(`${API_BASE_URL}/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query, num_results: numResults }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to perform search');
      }
      
      return await response.json();
    } catch (error) {
      console.error('API Service Error:', error);
      throw error;
    }
  },
  
  /**
   * Check API health
   * @returns {Promise} - Promise resolving to health status
   */
  checkHealth: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      
      if (!response.ok) {
        throw new Error('API health check failed');
      }
      
      return await response.json();
    } catch (error) {
      console.error('API Health Check Error:', error);
      throw error;
    }
  }
};

export default apiService;
