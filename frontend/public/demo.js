import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="app-container">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
          <div className="container">
            <Link className="navbar-brand" to="/">Web Research Agent</Link>
            <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <Link className="nav-link" to="/">Home</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/about">About</Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>
        
        <main className="container py-4">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/results" element={<ResultsPage />} />
            <Route path="/about" element={<AboutPage />} />
          </Routes>
        </main>
        
        <footer className="footer py-3 bg-dark text-white">
          <div className="container text-center">
            <span>© {new Date().getFullYear()} Web Research Agent</span>
          </div>
        </footer>
      </div>
    </Router>
  );
}

// HomePage Component
function HomePage() {
  const [query, setQuery] = React.useState('');
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState(null);
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    // In a real implementation, this would call the backend API
    setIsLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      setIsLoading(false);
      window.location.href = '/results?query=' + encodeURIComponent(query);
    }, 1000);
  };
  
  return (
    <div className="row justify-content-center">
      <div className="col-md-8">
        <div className="card shadow-sm">
          <div className="card-body p-4">
            <h2 className="text-center mb-4">Web Research Assistant</h2>
            <p className="text-center mb-4">
              Enter your research query and let our AI-powered agent find and synthesize information from across the web.
            </p>
            
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <input
                  type="text"
                  className="form-control form-control-lg"
                  placeholder="What would you like to research?"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  required
                />
              </div>
              <div className="d-grid">
                <button 
                  type="submit" 
                  className="btn btn-primary btn-lg"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      Researching...
                    </>
                  ) : 'Research'}
                </button>
              </div>
            </form>
            
            {error && (
              <div className="alert alert-danger mt-3">
                {error}
              </div>
            )}
            
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
    </div>
  );
}

// ResultsPage Component
function ResultsPage() {
  const [isLoading, setIsLoading] = React.useState(true);
  const [results, setResults] = React.useState(null);
  
  React.useEffect(() => {
    // Get query from URL
    const params = new URLSearchParams(window.location.search);
    const query = params.get('query');
    
    if (!query) {
      window.location.href = '/';
      return;
    }
    
    // Simulate API response
    setTimeout(() => {
      setResults({
        query: query,
        summary: `This is a comprehensive analysis of "${query}". The research shows multiple perspectives and insights on this topic.`,
        topics: [
          {
            name: 'Overview',
            points: [
              { text: 'This is a key point about the topic that provides general context.', source: 'Example Source', url: '#' },
              { text: 'Another important aspect of the topic that helps understand the basics.', source: 'Example Source', url: '#' }
            ]
          },
          {
            name: 'Analysis',
            points: [
              { text: 'A detailed analysis of a specific aspect of the topic.', source: 'Example Source', url: '#' },
              { text: 'Another analytical point that provides deeper insights.', source: 'Example Source', url: '#' }
            ]
          }
        ],
        conclusions: [
          'Based on the research, several key insights emerge about this topic.',
          'Further research may be needed to fully address all aspects of this query.',
          'The information gathered shows both consensus and diverging viewpoints.'
        ],
        sources: [
          { title: 'Example Source 1', url: '#', relevance: 0.85, reliability: 0.9 },
          { title: 'Example Source 2', url: '#', relevance: 0.75, reliability: 0.8 }
        ]
      });
      setIsLoading(false);
    }, 2000);
  }, []);
  
  if (isLoading) {
    return (
      <div className="text-center my-5">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p className="mt-3">Researching your query... This may take a moment.</p>
      </div>
    );
  }
  
  if (!results) {
    return (
      <div className="alert alert-warning">
        No results found. <Link to="/">Try another search</Link>
      </div>
    );
  }
  
  return (
    <div className="card shadow-sm">
      <div className="card-body p-4">
        <h2 className="mb-4">Research Results: {results.query}</h2>
        <Link to="/" className="btn btn-outline-primary mb-4">New Search</Link>
        
        <div className="mb-4">
          <h3>Summary</h3>
          <p>{results.summary}</p>
        </div>
        
        <div className="mb-4">
          <h3>Key Findings</h3>
          {results.topics.map((topic, index) => (
            <div key={index} className="mb-4">
              <h4 className="border-bottom pb-2">{topic.name}</h4>
              {topic.points.map((point, pointIndex) => (
                <div key={pointIndex} className="card mb-3">
                  <div className="card-body">
                    <p>{point.text}</p>
                    <small className="text-muted">
                      Source: <a href={point.url} target="_blank" rel="noopener noreferrer">{point.source}</a>
                    </small>
                  </div>
                </div>
              ))}
            </div>
          ))}
        </div>
        
        <div className="mb-4 bg-light p-3 rounded">
          <h3>Conclusions</h3>
          <ul>
            {results.conclusions.map((conclusion, index) => (
              <li key={index} className="mb-2">{conclusion}</li>
            ))}
          </ul>
        </div>
        
        <div className="mb-4">
          <h3>Sources</h3>
          <div className="list-group">
            {results.sources.map((source, index) => (
              <div key={index} className="list-group-item">
                <h5>
                  <a href={source.url} target="_blank" rel="noopener noreferrer">{source.title}</a>
                </h5>
                <div className="d-flex justify-content-between">
                  <small>Relevance: {Math.round(source.relevance * 100)}%</small>
                  <small>Reliability: {Math.round(source.reliability * 100)}%</small>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// AboutPage Component
function AboutPage() {
  return (
    <div className="card shadow-sm">
      <div className="card-body p-4">
        <h2 className="mb-4">About Web Research Agent</h2>
        
        <div className="mb-4">
          <h3>What is Web Research Agent?</h3>
          <p>
            Web Research Agent is an AI-powered tool designed to automate web research tasks. 
            It can search the web, find relevant information, extract data from websites, 
            and compile comprehensive research reports based on your queries.
          </p>
        </div>
        
        <div className="mb-4">
          <h3>How It Works</h3>
          <ol>
            <li className="mb-2">
              <strong>Query Analysis:</strong> The agent analyzes your research query to understand 
              the intent and information needs.
            </li>
            <li className="mb-2">
              <strong>Web Search:</strong> It performs targeted web searches to find relevant information 
              sources.
            </li>
            <li className="mb-2">
              <strong>Content Extraction:</strong> The agent visits the most promising websites and 
              extracts relevant content.
            </li>
            <li className="mb-2">
              <strong>Content Analysis:</strong> It analyzes the extracted content for relevance, 
              reliability, and key information.
            </li>
            <li className="mb-2">
              <strong>Information Synthesis:</strong> Finally, it combines information from multiple 
              sources into a coherent research report.
            </li>
          </ol>
        </div>
        
        <div className="text-center mt-5">
          <Link to="/" className="btn btn-primary btn-lg">Try It Now</Link>
        </div>
      </div>
    </div>
  );
}

export default App;
