import React from 'react';
import { Link } from 'react-router-dom';

function AboutPage() {
  return (
    <div className="results-container">
      <h2>About Web Research Agent</h2>
      
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
          <li>
            <strong>Query Analysis:</strong> The agent analyzes your research query to understand 
            the intent and information needs.
          </li>
          <li>
            <strong>Web Search:</strong> It performs targeted web searches to find relevant information 
            sources.
          </li>
          <li>
            <strong>Content Extraction:</strong> The agent visits the most promising websites and 
            extracts relevant content.
          </li>
          <li>
            <strong>Content Analysis:</strong> It analyzes the extracted content for relevance, 
            reliability, and key information.
          </li>
          <li>
            <strong>Information Synthesis:</strong> Finally, it combines information from multiple 
            sources into a coherent research report.
          </li>
        </ol>
      </div>
      
      <div className="mb-4">
        <h3>Features</h3>
        <ul>
          <li>Automated web research across multiple sources</li>
          <li>Content relevance and reliability assessment</li>
          <li>Key information extraction and summarization</li>
          <li>Organized presentation of research findings</li>
          <li>Source tracking and citation</li>
        </ul>
      </div>
      
      <div className="mb-4">
        <h3>Use Cases</h3>
        <ul>
          <li>Academic research and literature reviews</li>
          <li>Market research and competitive analysis</li>
          <li>Fact-checking and information verification</li>
          <li>News monitoring and trend analysis</li>
          <li>Learning about new topics and concepts</li>
        </ul>
      </div>
      
      <div className="text-center mt-5">
        <Link to="/" className="btn btn-primary">Try It Now</Link>
      </div>
    </div>
  );
}

export default AboutPage;
