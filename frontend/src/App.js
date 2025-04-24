import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import ResultsPage from './pages/ResultsPage';
import AboutPage from './pages/AboutPage';

function App() {
  const [researchResults, setResearchResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  return (
    <Router>
      <div className="app-container">
        <Header />
        <main className="container py-4">
          <Routes>
            <Route 
              path="/" 
              element={
                <HomePage 
                  setResearchResults={setResearchResults}
                  setIsLoading={setIsLoading}
                  setError={setError}
                />
              } 
            />
            <Route 
              path="/results" 
              element={
                <ResultsPage 
                  researchResults={researchResults}
                  isLoading={isLoading}
                  error={error}
                />
              } 
            />
            <Route path="/about" element={<AboutPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
