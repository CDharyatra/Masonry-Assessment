import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import apiService from '../services/apiService';

function ResultsPage({ researchResults, isLoading, error }) {
  const [apiStatus, setApiStatus] = useState('unknown');

  useEffect(() => {
    // Check API health when component mounts
    const checkApiHealth = async () => {
      try {
        const health = await apiService.checkHealth();
        setApiStatus(health.status === 'ok' ? 'online' : 'offline');
      } catch (error) {
        setApiStatus('offline');
        console.error('API health check failed:', error);
      }
    };

    checkApiHealth();
  }, []);

  if (isLoading) {
    return (
      <div className="results-container">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="ms-3 mb-0">Researching your query... This may take a moment.</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="results-container">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">Error!</h4>
          <p>{error}</p>
          <hr />
          <p className="mb-0">
            {apiStatus === 'offline' 
              ? 'The research service appears to be offline. Please try again later.' 
              : 'Please try again with a different query.'}
          </p>
          <Link to="/" className="btn btn-primary mt-3">Back to Search</Link>
        </div>
      </div>
    );
  }

  if (!researchResults || !researchResults.success || !researchResults.report) {
    return (
      <div className="results-container">
        <div className="alert alert-warning" role="alert">
          <h4 className="alert-heading">No Results</h4>
          <p>No research results are available. Please try a new search.</p>
          <Link to="/" className="btn btn-primary mt-3">Back to Search</Link>
        </div>
      </div>
    );
  }

  const { report } = researchResults;

  return (
    <div className="results-container">
      <div className="mb-4">
        <h2>Research Results: {report.query}</h2>
        <Link to="/" className="btn btn-outline-primary mt-2">New Search</Link>
      </div>

      {/* Summary Section */}
      <div className="mb-4">
        <h3>Summary</h3>
        <p>{report.summary}</p>
      </div>

      {/* Topics Section */}
      <div className="mb-4">
        <h3>Key Findings</h3>
        {report.topics && report.topics.map((topic, index) => (
          <div key={index} className="topic-section">
            <h4 className="topic-title">{topic.name}</h4>
            {topic.points && topic.points.map((point, pointIndex) => (
              <div key={pointIndex} className="key-point">
                <p>{point.text}</p>
                <div className="key-point-source">
                  Source: <a href={point.url} target="_blank" rel="noopener noreferrer">{point.source}</a>
                </div>
              </div>
            ))}
          </div>
        ))}
      </div>

      {/* Conclusions Section */}
      <div className="conclusion-section">
        <h3 className="conclusion-title">Conclusions</h3>
        <ul>
          {report.conclusions && report.conclusions.map((conclusion, index) => (
            <li key={index} className="conclusion-item">{conclusion}</li>
          ))}
        </ul>
      </div>

      {/* Sources Section */}
      <div className="mt-4">
        <h3>Sources</h3>
        <div className="list-group">
          {report.sources && report.sources.map((source, index) => (
            <div key={index} className="list-group-item">
              <h5 className="mb-1">
                <a href={source.url} target="_blank" rel="noopener noreferrer" className="source-title">
                  {source.title}
                </a>
              </h5>
              <p className="source-url mb-1">{source.url}</p>
              <div className="d-flex justify-content-between">
                <small>Relevance: {Math.round(source.relevance * 100)}%</small>
                <small>Reliability: {Math.round(source.reliability * 100)}%</small>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Search Results Section */}
      <div className="mt-4">
        <h3>Search Results</h3>
        <div className="list-group">
          {report.search_results && report.search_results.map((result, index) => (
            <div key={index} className="list-group-item">
              <h5 className="mb-1">
                <a href={result.url} target="_blank" rel="noopener noreferrer" className="source-title">
                  {result.title}
                </a>
              </h5>
              <p className="source-url mb-1">{result.url}</p>
              <p className="source-snippet">{result.snippet}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ResultsPage;
