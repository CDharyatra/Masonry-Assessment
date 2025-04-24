import sys
import os
from typing import Dict, Any, List, Optional
import re
import json

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

class ContentAnalyzerTool:
    """
    Tool for analyzing and processing content extracted from web pages.
    Evaluates relevance, reliability, and extracts key information.
    """
    
    def __init__(self):
        self.openai_api_key = Config.OPENAI_API_KEY
        
    def analyze_content(self, content: Dict[str, Any], query: str) -> Dict[str, Any]:
        """
        Analyze the content extracted from a web page.
        
        Args:
            content: Dictionary containing the scraped content
            query: The original search query
            
        Returns:
            Dictionary containing analysis results
        """
        if not content or not content.get('success', False):
            return {
                'success': False,
                'error': 'No valid content to analyze',
                'relevance_score': 0,
                'key_points': []
            }
        
        # Extract the main text content
        main_text = content.get('content', {}).get('main_text', '')
        if not main_text:
            return {
                'success': False,
                'error': 'No text content to analyze',
                'relevance_score': 0,
                'key_points': []
            }
        
        # Calculate relevance score
        relevance_score = self._calculate_relevance(main_text, query)
        
        # Extract key points
        key_points = self._extract_key_points(main_text, query)
        
        # Assess reliability
        reliability_score = self._assess_reliability(content)
        
        # Identify sentiment
        sentiment = self._analyze_sentiment(main_text)
        
        # Extract entities
        entities = self._extract_entities(main_text)
        
        return {
            'success': True,
            'relevance_score': relevance_score,
            'reliability_score': reliability_score,
            'key_points': key_points,
            'sentiment': sentiment,
            'entities': entities
        }
    
    def _calculate_relevance(self, text: str, query: str) -> float:
        """
        Calculate the relevance score of the content to the query.
        
        Args:
            text: The text content to analyze
            query: The original search query
            
        Returns:
            Relevance score between 0 and 1
        """
        # Simple relevance calculation based on term frequency
        query_terms = query.lower().split()
        text_lower = text.lower()
        
        # Count occurrences of query terms
        term_counts = {}
        for term in query_terms:
            # Use word boundaries to match whole words
            pattern = r'\b' + re.escape(term) + r'\b'
            count = len(re.findall(pattern, text_lower))
            term_counts[term] = count
        
        # Calculate average occurrence per term
        if not query_terms:
            return 0
        
        total_occurrences = sum(term_counts.values())
        avg_occurrence = total_occurrences / len(query_terms)
        
        # Normalize to a score between 0 and 1
        # Assuming a relevant document would have each term appear at least 3 times on average
        relevance_score = min(avg_occurrence / 3, 1.0)
        
        return relevance_score
    
    def _extract_key_points(self, text: str, query: str) -> List[str]:
        """
        Extract key points from the text that are relevant to the query.
        
        Args:
            text: The text content to analyze
            query: The original search query
            
        Returns:
            List of key points extracted from the text
        """
        # In a real implementation, this would use NLP or AI to extract key points
        # For this mock implementation, we'll use a simple approach
        
        # Split text into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Score sentences based on query term occurrence
        query_terms = query.lower().split()
        scored_sentences = []
        
        for sentence in sentences:
            if len(sentence) < 10:  # Skip very short sentences
                continue
                
            score = 0
            sentence_lower = sentence.lower()
            
            for term in query_terms:
                if term in sentence_lower:
                    score += 1
            
            # Boost score for sentences with multiple query terms
            if score > 1:
                score *= 1.5
                
            scored_sentences.append((sentence, score))
        
        # Sort sentences by score and take top ones
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [s[0] for s in scored_sentences[:5] if s[1] > 0]
        
        # If we don't have enough relevant sentences, include some based on position
        if len(top_sentences) < 3 and len(sentences) > 3:
            # Include first sentence (often contains key information)
            if sentences[0] not in top_sentences:
                top_sentences.append(sentences[0])
            
            # Include some sentences from the beginning and middle
            candidates = [sentences[i] for i in range(1, min(10, len(sentences)))]
            for candidate in candidates:
                if len(candidate) > 30 and candidate not in top_sentences:
                    top_sentences.append(candidate)
                    if len(top_sentences) >= 5:
                        break
        
        return top_sentences
    
    def _assess_reliability(self, content: Dict[str, Any]) -> float:
        """
        Assess the reliability of the content source.
        
        Args:
            content: Dictionary containing the scraped content and metadata
            
        Returns:
            Reliability score between 0 and 1
        """
        # In a real implementation, this would use various signals to assess reliability
        # For this mock implementation, we'll use a simple heuristic approach
        
        reliability_score = 0.5  # Default neutral score
        
        # Check if metadata exists
        metadata = content.get('metadata', {})
        if not metadata:
            return reliability_score
        
        # Boost score for known reliable domains
        site_name = metadata.get('site_name', '')
        url = metadata.get('url', '')
        
        reliable_domains = [
            'wikipedia.org', 'nytimes.com', 'bbc.com', 'reuters.com', 
            'nature.com', 'science.org', 'scientificamerican.com',
            'economist.com', 'washingtonpost.com', 'theguardian.com'
        ]
        
        for domain in reliable_domains:
            if domain in url or domain in site_name.lower():
                reliability_score += 0.3
                break
        
        # Boost score if author is provided
        if metadata.get('author'):
            reliability_score += 0.1
        
        # Boost score if published date is recent
        if metadata.get('published_date'):
            reliability_score += 0.1
        
        # Cap at 1.0
        reliability_score = min(reliability_score, 1.0)
        
        return reliability_score
    
    def _analyze_sentiment(self, text: str) -> str:
        """
        Analyze the sentiment of the text.
        
        Args:
            text: The text content to analyze
            
        Returns:
            Sentiment classification (positive, negative, or neutral)
        """
        # In a real implementation, this would use NLP or AI for sentiment analysis
        # For this mock implementation, we'll use a simple keyword approach
        
        positive_words = ['good', 'great', 'excellent', 'positive', 'beneficial', 
                         'advantage', 'success', 'improve', 'better', 'best']
        
        negative_words = ['bad', 'poor', 'negative', 'problem', 'issue', 'concern',
                         'risk', 'fail', 'worse', 'worst']
        
        text_lower = text.lower()
        
        positive_count = sum(text_lower.count(' ' + word + ' ') for word in positive_words)
        negative_count = sum(text_lower.count(' ' + word + ' ') for word in negative_words)
        
        if positive_count > negative_count * 1.5:
            return 'positive'
        elif negative_count > positive_count * 1.5:
            return 'negative'
        else:
            return 'neutral'
    
    def _extract_entities(self, text: str) -> List[Dict[str, str]]:
        """
        Extract named entities from the text.
        
        Args:
            text: The text content to analyze
            
        Returns:
            List of extracted entities with their types
        """
        # In a real implementation, this would use NLP for named entity recognition
        # For this mock implementation, we'll return a placeholder
        
        # Just return a few example entities that might be found in the text
        # In a real implementation, these would be extracted using NER
        return [
            {'text': 'Example Organization', 'type': 'ORGANIZATION'},
            {'text': 'John Smith', 'type': 'PERSON'},
            {'text': 'New York', 'type': 'LOCATION'}
        ]
    
    def analyze_multiple_contents(self, contents: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """
        Analyze multiple content items and return analysis results.
        
        Args:
            contents: List of dictionaries containing scraped content
            query: The original search query
            
        Returns:
            List of dictionaries containing analysis results
        """
        results = []
        
        for content in contents:
            analysis = self.analyze_content(content, query)
            results.append({
                'content': content,
                'analysis': analysis
            })
        
        # Sort results by relevance score
        results.sort(key=lambda x: x['analysis'].get('relevance_score', 0), reverse=True)
        
        return results
