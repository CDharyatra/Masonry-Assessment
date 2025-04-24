import sys
import os
from typing import Dict, Any, List, Optional
import json

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from tools.web_search import WebSearchTool
from tools.web_scraper import WebScraperTool
from tools.content_analyzer import ContentAnalyzerTool

class InformationSynthesisTool:
    """
    Tool for synthesizing information from multiple sources into a coherent research report.
    Combines, organizes, and summarizes information to answer the original query.
    """
    
    def __init__(self):
        self.openai_api_key = Config.OPENAI_API_KEY
        
    def synthesize_information(self, analyzed_contents: List[Dict[str, Any]], query: str) -> Dict[str, Any]:
        """
        Synthesize information from multiple analyzed content sources.
        
        Args:
            analyzed_contents: List of dictionaries containing content and analysis results
            query: The original search query
            
        Returns:
            Dictionary containing the synthesized information
        """
        if not analyzed_contents:
            return {
                'success': False,
                'error': 'No content to synthesize',
                'report': None
            }
        
        # Extract key information from each source
        sources = []
        key_points = []
        
        for item in analyzed_contents:
            content = item.get('content', {})
            analysis = item.get('analysis', {})
            
            if not content or not analysis:
                continue
                
            # Skip low-relevance content
            if analysis.get('relevance_score', 0) < 0.2:
                continue
                
            # Extract metadata
            metadata = content.get('metadata', {})
            url = content.get('url', '')
            title = metadata.get('title', 'Untitled')
            
            # Add source information
            sources.append({
                'title': title,
                'url': url,
                'relevance': analysis.get('relevance_score', 0),
                'reliability': analysis.get('reliability_score', 0)
            })
            
            # Add key points
            points = analysis.get('key_points', [])
            for point in points:
                key_points.append({
                    'text': point,
                    'source': title,
                    'url': url
                })
        
        # Organize information by topic
        topics = self._organize_by_topic(key_points, query)
        
        # Generate summary
        summary = self._generate_summary(key_points, query)
        
        # Generate conclusions
        conclusions = self._generate_conclusions(key_points, query)
        
        # Compile the final report
        report = {
            'query': query,
            'summary': summary,
            'topics': topics,
            'conclusions': conclusions,
            'sources': sources
        }
        
        return {
            'success': True,
            'report': report
        }
    
    def _organize_by_topic(self, key_points: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """
        Organize key points by topic.
        
        Args:
            key_points: List of key points extracted from content
            query: The original search query
            
        Returns:
            List of topics with associated key points
        """
        # In a real implementation, this would use NLP or AI to cluster points by topic
        # For this mock implementation, we'll use a simple approach
        
        # Extract query terms to use as potential topics
        query_terms = query.lower().split()
        potential_topics = [term for term in query_terms if len(term) > 3]
        
        # Add some generic topics
        generic_topics = ['Overview', 'Background', 'Analysis', 'Impact', 'Future']
        potential_topics.extend(generic_topics)
        
        # Assign points to topics
        topics = {}
        
        for point in key_points:
            point_text = point['text'].lower()
            assigned = False
            
            # Try to assign to a specific topic
            for topic in potential_topics:
                if topic.lower() in point_text:
                    if topic not in topics:
                        topics[topic] = []
                    topics[topic].append(point)
                    assigned = True
                    break
            
            # If not assigned, put in Overview
            if not assigned:
                if 'Overview' not in topics:
                    topics['Overview'] = []
                topics['Overview'].append(point)
        
        # Convert to list format
        result = []
        for topic, points in topics.items():
            result.append({
                'name': topic.capitalize(),
                'points': points
            })
        
        return result
    
    def _generate_summary(self, key_points: List[Dict[str, Any]], query: str) -> str:
        """
        Generate a summary of the information.
        
        Args:
            key_points: List of key points extracted from content
            query: The original search query
            
        Returns:
            Summary text
        """
        # In a real implementation, this would use NLP or AI to generate a summary
        # For this mock implementation, we'll use a simple approach
        
        if not key_points:
            return f"No relevant information found for '{query}'."
        
        # Use the first few key points to create a summary
        summary_points = key_points[:3]
        summary_text = " ".join([point['text'] for point in summary_points])
        
        # Add an introduction
        introduction = f"Based on research about '{query}', the following information was found. "
        
        return introduction + summary_text
    
    def _generate_conclusions(self, key_points: List[Dict[str, Any]], query: str) -> List[str]:
        """
        Generate conclusions based on the information.
        
        Args:
            key_points: List of key points extracted from content
            query: The original search query
            
        Returns:
            List of conclusion statements
        """
        # In a real implementation, this would use NLP or AI to generate conclusions
        # For this mock implementation, we'll return generic conclusions
        
        if not key_points:
            return ["Insufficient information available to draw conclusions."]
        
        # Generate generic conclusions
        conclusions = [
            f"Research on '{query}' reveals multiple perspectives and insights.",
            "The information gathered shows both consensus and diverging viewpoints on this topic.",
            "Further research may be needed to fully address all aspects of this query."
        ]
        
        return conclusions
    
    def generate_research_report(self, query: str) -> Dict[str, Any]:
        """
        Generate a complete research report for the given query.
        This method orchestrates the entire research process.
        
        Args:
            query: The research query
            
        Returns:
            Dictionary containing the research report
        """
        # Initialize tools
        search_tool = WebSearchTool()
        scraper_tool = WebScraperTool()
        analyzer_tool = ContentAnalyzerTool()
        
        # Step 1: Perform web search
        search_results = search_tool.search(query, num_results=Config.SEARCH_RESULT_COUNT)
        
        if not search_results:
            return {
                'success': False,
                'error': 'No search results found',
                'report': None
            }
        
        # Step 2: Scrape content from search results
        urls = [result['url'] for result in search_results]
        scraped_contents = scraper_tool.scrape_multiple_urls(urls)
        
        if not scraped_contents:
            return {
                'success': False,
                'error': 'Failed to scrape content from search results',
                'report': None
            }
        
        # Step 3: Analyze content
        analyzed_contents = analyzer_tool.analyze_multiple_contents(scraped_contents, query)
        
        if not analyzed_contents:
            return {
                'success': False,
                'error': 'Failed to analyze content',
                'report': None
            }
        
        # Step 4: Synthesize information
        synthesis_result = self.synthesize_information(analyzed_contents, query)
        
        # Add search results to the report
        if synthesis_result['success'] and synthesis_result['report']:
            synthesis_result['report']['search_results'] = search_results
        
        return synthesis_result
