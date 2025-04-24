import apiService from '../services/apiService';

// Update the HomePage component to use the API service
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function HomePage({ setResearchResults, setIsLoading, setError }) {
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      return;
    }
    
    setIsLoading(true);
    setError(null);
    
    try {
      // Use the API service to perform research
      const results = await apiService.performResearch(query);
      setResearchResults(results);
      navigate('/results');
    } catch (error) {
      console.error('Error performing research:', error);
      setError(error.message || 'An error occurred while performing research');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="row justify-content-center">
      <div className="col-md-10 col-lg-8">
        <div className="search-container">
          <h2 className="text-center mb-4">Research Assistant</h2>
          <p className="text-center mb-4">
            Enter your research query and let our AI-powered agent find and synthesize information from across the web.
          </p>
          
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <input
                type="text"
                className="form-control search-input"
                placeholder="Enter your research query..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                required
              />
            </div>
            <div className="d-grid gap-2">
              <button type="submit" className="btn btn-primary search-button">
                Research
              </button>
            </div>
          </form>
          
          <div className="mt-4">
            <h5>Example queries:</h5>
            <ul>
              <li>What are the environmental impacts of electric vehicles?</li>
              <li>How does artificial intelligence impact job markets?</li>
              <li>What are the latest developments in renewable energy?</li>
              <li>Compare different approaches to machine learning</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
