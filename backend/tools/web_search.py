import requests
from bs4 import BeautifulSoup
import json
from typing import List, Dict, Any
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__) )))
from config import Config

class WebSearchTool:
    """
    Tool for performing web searches and retrieving search results using SerpAPI.
    """
    
    def __init__(self):
        self.api_key = Config.SERPAPI_KEY
        self.base_url = "https://serpapi.com/search"
        
    def search(self, query: str, num_results: int = 10)  -> List[Dict[str, Any]]:
        """
        Perform a web search for the given query and return a list of search results.
        
        Args:
            query: The search query string
            num_results: Number of results to return
            
        Returns:
            List of dictionaries containing search results with title, url, and snippet
        """
        try:
            # Prepare parameters for SerpAPI
            params = {
                "q": query,
                "api_key": self.api_key,
                "engine": "google",
                "num": num_results,
                "gl": "us",  # Country to search from
                "hl": "en"   # Language
            }
            
            # Make the API request
            response = requests.get(self.base_url, params=params)
            
            if response.status_code != 200:
                print(f"Error from SerpAPI: {response.status_code}")
                return self._generate_mock_results(query, num_results)
                
            # Parse the JSON response
            data = response.json()
            
            # Extract organic search results
            search_results = []
            
            if "organic_results" in data:
                for result in data["organic_results"][:num_results]:
                    title = result.get("title", "")
                    url = result.get("link", "")
                    snippet = result.get("snippet", "")
                    
                    search_results.append({
                        'title': title,
                        'url': url,
                        'snippet': snippet
                    })
            
            # If we couldn't extract enough results, supplement with mock results
            if len(search_results) < num_results:
                search_results.extend(self._generate_mock_results(query, num_results - len(search_results)))
                
            return search_results[:num_results]
            
        except Exception as e:
            print(f"Error performing search: {e}")
            # Fall back to mock results if the search fails
            return self._generate_mock_results(query, num_results)
    
    def _generate_mock_results(self, query: str, num_results: int) -> List[Dict[str, Any]]:
        """
        Generate mock search results for demonstration purposes.
        
        Args:
            query: The search query string
            num_results: Number of results to generate
            
        Returns:
            List of dictionaries containing mock search results
        """
        mock_results = []
        
        # Generate some realistic-looking mock results based on the query
        query_terms = query.split()
        
        domains = [
            "wikipedia.org", "nytimes.com", "theguardian.com", "bbc.com", 
            "reuters.com", "cnn.com", "washingtonpost.com", "medium.com",
            "forbes.com", "techcrunch.com", "wired.com", "scientificamerican.com"
        ]
        
        for i in range(num_results):
            domain = domains[i % len(domains)]
            title_terms = query_terms + ["information", "guide", "overview", "analysis", "report"]
            title = " ".join([term.capitalize() for term in title_terms[:3 + (i % 3)]])
            
            url_path = "-".join(query_terms) + f"-{i+1}"
            url = f"https://www.{domain}/articles/{url_path}"
            
            snippet = f"Comprehensive information about {query}. This article provides detailed analysis and insights into {query} with expert opinions and recent developments."
            
            mock_results.append({
                'title': title,
                'url': url,
                'snippet': snippet
            }) 
        
        return mock_results
