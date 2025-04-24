## Overview

Web Research Agent is an AI-powered tool designed to automate web research tasks. It searches the web, finds relevant information, extracts data from websites, and compiles comprehensive research reports based on user queries.

Here is the Loom Video - https://www.loom.com/share/252e0631ef5040a8b393f256ee5af502?sid=7e9af5fb-c351-4b61-b69c-23a52f87d8e1
Here is the live website link - https://masonry-assessment-frontend.onrender.com

## Features

- **Query Analysis**: Understands the intent behind user research queries
- **Web Search**: Searches the web for relevant information using SerpAPI
- **Content Extraction**: Scrapes and extracts content from multiple websites
- **Content Analysis**: Evaluates content for relevance and reliability
- **Information Synthesis**: Combines information from multiple sources into coherent reports

## Architecture

The Web Research Agent consists of two main components:

1. **Backend**: Python-based API with core research functionality
2. **Frontend**: React-based user interface for interacting with the agent

### Backend Components

- `web_search.py`: Tool for performing web searches using SerpAPI
- `web_scraper.py`: Tool for extracting content from web pages
- `content_analyzer.py`: Tool for analyzing content relevance and reliability
- `information_synthesis.py`: Tool for combining information from multiple sources
- `agent.py`: Main agent class that orchestrates the research process
- `app.py`: Flask API for frontend communication

### Frontend Components

- React components for user interface
- API service for communication with backend
- Responsive design for desktop and mobile devices

## Installation

### Prerequisites

- Python 3.10+
- Node.js 14+
- npm 6+
- SerpAPI key (for web search functionality)

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/CDharyatra/Masonry-Assessment.git
cd web-research-agent

# Install backend dependencies
cd backend
pip install flask requests beautifulsoup4 openai python-dotenv flask-cors

# Set up environment variables
echo "SERPAPI_KEY=your-serpapi-key" > .env
```

### Frontend Setup

```bash
# Install frontend dependencies
cd ../frontend
npm install
```

## Usage

### Running the Application

#### Backend

```bash
# Start the backend server
cd backend
python app.py
```

The backend server will start running on http://localhost:5000

#### Frontend

**Option 1: Using the HTML file directly**
Simply open the `frontend/index.html` file in your web browser.

**Option 2: Building with webpack (requires additional setup)**
```bash
cd frontend
npm install --save-dev webpack webpack-cli webpack-dev-server babel-loader @babel/core @babel/preset-env @babel/preset-react style-loader css-loader html-webpack-plugin
npm run start
```

### Using the Web Research Agent

1. Enter your research query in the search box
2. Click "Research" to start the research process
3. View the comprehensive research report with:
   - Summary of findings
   - Key points organized by topic
   - Conclusions drawn from the research
   - Sources with relevance and reliability scores

## How It Works

### Query Processing Flow

1. **Query Analysis**: The agent analyzes the query to understand the research intent
2. **Web Search**: The agent searches the web using SerpAPI to find relevant sources
3. **Content Extraction**: The agent visits each source and extracts relevant content
4. **Content Analysis**: The agent evaluates content for relevance and reliability
5. **Information Synthesis**: The agent combines information into a coherent report

### Tool Integration

The Web Research Agent integrates with the following external tools:

1. **SerpAPI**: For performing web searches and retrieving search results
2. **BeautifulSoup**: For parsing and extracting content from web pages
3. **OpenAI API** (optional): For enhancing content analysis and synthesis

## Error Handling

The Web Research Agent includes robust error handling:

- **Search Failures**: Falls back to mock results if web search fails
- **Content Extraction Issues**: Skips problematic sources and continues with available content
- **API Limits**: Gracefully handles API rate limiting with appropriate user feedback
- **Network Issues**: Provides clear error messages and recovery options

## Development

### Backend Development

To extend the backend functionality:

1. Add new tools in the `tools` directory
2. Update the `agent.py` file to incorporate new tools
3. Add new API endpoints in `app.py` as needed

### Frontend Development

To extend the frontend functionality:

1. Modify React components in the `src` directory
2. Update API service to communicate with new backend endpoints
3. Enhance UI/UX as needed

## Testing

To test the application:

```bash
# Test the backend
cd backend
python -m unittest discover tests

# Test the frontend
cd ../frontend
npm test
```

## Deployment

### Backend Deployment

The backend can be deployed to any server that supports Python:

```bash
# Install production dependencies
pip install gunicorn

# Start the server
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend Deployment

The frontend can be deployed to any static hosting service:

```bash
# Build the production version
npm run build


## Author

Dharyatra
