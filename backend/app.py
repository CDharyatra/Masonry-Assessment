import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import Config
from tools.information_synthesis import InformationSynthesisTool

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the research agent
synthesis_tool = InformationSynthesisTool()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Web Research Agent API is running'
    })

@app.route('/api/research', methods=['POST'])
def research():
    """
    Endpoint to perform research based on a query
    
    Request body:
    {
        "query": "Research query string"
    }
    """
    data = request.json
    
    if not data or 'query' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing query parameter'
        }), 400
    
    query = data['query']
    
    if not query or len(query.strip()) == 0:
        return jsonify({
            'success': False,
            'error': 'Query cannot be empty'
        }), 400
    
    try:
        # Generate research report
        result = synthesis_tool.generate_research_report(query)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/search', methods=['POST'])
def search():
    """
    Endpoint to perform just a web search
    
    Request body:
    {
        "query": "Search query string",
        "num_results": 10  # Optional
    }
    """
    data = request.json
    
    if not data or 'query' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing query parameter'
        }), 400
    
    query = data['query']
    num_results = data.get('num_results', Config.SEARCH_RESULT_COUNT)
    
    if not query or len(query.strip()) == 0:
        return jsonify({
            'success': False,
            'error': 'Query cannot be empty'
        }), 400
    
    try:
        from tools.web_search import WebSearchTool
        search_tool = WebSearchTool()
        
        # Perform search
        results = search_tool.search(query, num_results=num_results)
        
        return jsonify({
            'success': True,
            'results': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host=Config.API_HOST, port=Config.API_PORT, debug=True)
