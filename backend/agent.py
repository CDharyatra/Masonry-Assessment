import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from tools.web_search import WebSearchTool
from tools.web_scraper import WebScraperTool
from tools.content_analyzer import ContentAnalyzerTool
from tools.information_synthesis import InformationSynthesisTool

class WebResearchAgent:
    """
    Main Web Research Agent class that orchestrates the research process.
    This class serves as the central controller for the entire research workflow.
    """
    
    def __init__(self):
        """Initialize the Web Research Agent with all required tools."""
        self.search_tool = WebSearchTool()
        self.scraper_tool = WebScraperTool()
        self.analyzer_tool = ContentAnalyzerTool()
        self.synthesis_tool = InformationSynthesisTool()
    
    def process_query(self, query: str) -> dict:
        """
        Process a research query and generate a comprehensive report.
        
        Args:
            query: The research query from the user
            
        Returns:
            Dictionary containing the research report and status
        """
        try:
            # Step 1: Analyze the query to understand intent
            query_intent = self._analyze_query_intent(query)
            
            # Step 2: Generate research report using the synthesis tool
            # The synthesis tool will internally call the other tools as needed
            result = self.synthesis_tool.generate_research_report(query)
            
            # Add query intent information to the result
            if result['success'] and result['report']:
                result['report']['query_intent'] = query_intent
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error processing query: {str(e)}",
                'report': None
            }
    
    def _analyze_query_intent(self, query: str) -> dict:
        """
        Analyze the intent behind the user's query.
        
        Args:
            query: The research query
            
        Returns:
            Dictionary containing query intent information
        """
        # In a real implementation, this would use NLP or AI to analyze query intent
        # For this mock implementation, we'll use a simple approach
        
        query_lower = query.lower()
        
        # Determine query type
        query_type = 'informational'  # Default type
        
        if any(term in query_lower for term in ['how to', 'steps', 'guide', 'tutorial']):
            query_type = 'instructional'
        elif any(term in query_lower for term in ['compare', 'difference', 'versus', 'vs']):
            query_type = 'comparative'
        elif any(term in query_lower for term in ['news', 'recent', 'latest', 'update']):
            query_type = 'news'
        elif any(term in query_lower for term in ['history', 'origin', 'background']):
            query_type = 'historical'
        
        # Determine information needs
        needs_facts = True
        needs_opinions = 'opinion' in query_lower or 'review' in query_lower
        needs_recent = any(term in query_lower for term in ['recent', 'latest', 'new', 'current'])
        needs_historical = any(term in query_lower for term in ['history', 'origin', 'background', 'evolution'])
        
        return {
            'query_type': query_type,
            'information_needs': {
                'facts': needs_facts,
                'opinions': needs_opinions,
                'recent': needs_recent,
                'historical': needs_historical
            }
        }
