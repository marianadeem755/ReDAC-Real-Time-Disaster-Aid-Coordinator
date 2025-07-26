import requests
import json
from typing import List, Dict
from config import SERPER_API_KEY, DISASTER_KEYWORDS
import time

class NewsAgent:
    """
    NEWS AGENT: Fetches disaster-related news
    This agent searches for news about disasters near the user's location
    Now includes DuckDuckGo backup when Serper fails!
    """
    
    def __init__(self):
        self.serper_api_key = SERPER_API_KEY
        self.serper_url = "https://google.serper.dev/news"
    
    def search_disaster_news(self, location: str, max_results: int = 5) -> List[Dict]:
        """
        Search for disaster news related to a specific location
        Uses Serper API first, falls back to DuckDuckGo if needed
        
        Args:
            location: User's location (e.g., "New York", "California")
            max_results: Maximum number of news articles to return
        
        Returns:
            List of news articles with title, snippet, and link
        """
        news_articles = []
        
        # Create search queries combining location with disaster keywords
        search_queries = [
            f"{location} disaster emergency alert",
            f"{location} earthquake flood hurricane",
            f"{location} weather warning evacuation"
        ]
        
        # Try Serper API first
        if self.serper_api_key:
            print("🔍 Using Serper API for news search...")
            for query in search_queries:
                try:
                    articles = self._fetch_serper_news(query, max_results//len(search_queries))
                    news_articles.extend(articles)
                except Exception as e:
                    print(f"Error fetching Serper news for query '{query}': {e}")
        
        # If no results from Serper or no API key, try DuckDuckGo
        if not news_articles:
            print("🦆 Falling back to DuckDuckGo search...")
            for query in search_queries:
                try:
                    articles = self._fetch_duckduckgo_news(query, max_results//len(search_queries))
                    news_articles.extend(articles)
                except Exception as e:
                    print(f"Error fetching DuckDuckGo news for query '{query}': {e}")
        
        # If still no results, use mock data
        if not news_articles:
            print("📰 Using mock news data for testing...")
            news_articles = self._get_mock_news(location)
        
        # Remove duplicates and return top results
        unique_articles = self._remove_duplicates(news_articles)
        return unique_articles[:max_results]
    
    def _fetch_serper_news(self, query: str, num_results: int) -> List[Dict]:
        """
        Fetch news from Serper API
        """
        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'q': query,
            'num': num_results,
            'hl': 'en',
            'gl': 'us'
        }
        
        response = requests.post(self.serper_url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        articles = []
        
        if 'news' in data:
            for item in data['news']:
                articles.append({
                    'title': item.get('title', ''),
                    'snippet': item.get('snippet', ''),
                    'link': item.get('link', ''),
                    'source': item.get('source', ''),
                    'date': item.get('date', ''),
                    'search_engine': 'Serper/Google'
                })
        
        return articles
    
    def _fetch_duckduckgo_news(self, query: str, num_results: int) -> List[Dict]:
        """
        Fetch news using DuckDuckGo (no API key required!)
        This is a backup method when Serper fails
        """
        try:
            # Try importing duckduckgo_search
            try:
                from duckduckgo_search import DDGS
            except ImportError:
                print("⚠️ duckduckgo_search not installed. Install with: pip install duckduckgo_search")
                return []
            
            # Search using DuckDuckGo
            with DDGS() as ddgs:
                results = list(ddgs.news(query, max_results=num_results))
                
                articles = []
                for item in results:
                    articles.append({
                        'title': item.get('title', ''),
                        'snippet': item.get('body', '')[:200] + '...' if len(item.get('body', '')) > 200 else item.get('body', ''),
                        'link': item.get('url', ''),
                        'source': item.get('source', 'DuckDuckGo'),
                        'date': item.get('date', 'Recent'),
                        'search_engine': 'DuckDuckGo'
                    })
                
                return articles
                
        except Exception as e:
            print(f"DuckDuckGo search failed: {e}")
            return []
    
    def _get_mock_news(self, location: str) -> List[Dict]:
        """
        Mock news data for testing when no APIs work
        """
        return [
            {
                'title': f'Weather Monitoring Update - {location}',
                'snippet': 'Local emergency services are monitoring weather conditions. No immediate threats detected, but residents should stay informed about changing conditions.',
                'link': 'https://example.com/mock-news-1',
                'source': 'Mock Emergency Services',
                'date': '1 hour ago',
                'search_engine': 'Mock Data'
            },
            {
                'title': f'Disaster Preparedness Reminder - {location} Area',
                'snippet': 'Authorities remind residents to keep emergency kits updated and review family emergency plans. Regular preparedness helps ensure community safety.',
                'link': 'https://example.com/mock-news-2',
                'source': 'Mock Local Authority',
                'date': '3 hours ago',
                'search_engine': 'Mock Data'
            },
            {
                'title': f'Infrastructure Status Report - {location}',
                'snippet': 'All critical infrastructure systems are operating normally. Emergency services report no significant incidents requiring public attention.',
                'link': 'https://example.com/mock-news-3',
                'source': 'Mock Infrastructure Dept',
                'date': '5 hours ago',
                'search_engine': 'Mock Data'
            }
        ]
    
    def _remove_duplicates(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on title similarity"""
        unique_articles = []
        seen_titles = set()
        
        for article in articles:
            # Create a normalized title for comparison
            title_key = article['title'].lower().strip()[:50]  # First 50 chars
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_articles.append(article)
        
        return unique_articles
    
    def format_news_for_analysis(self, articles: List[Dict]) -> str:
        """
        Format news articles into a string for AI analysis
        """
        if not articles:
            return "No recent news articles found."
        
        formatted_news = "Recent News Articles:\n\n"
        for i, article in enumerate(articles, 1):
            formatted_news += f"{i}. {article['title']}\n"
            formatted_news += f"   {article['snippet']}\n"
            formatted_news += f"   Source: {article['source']} | {article['date']}\n"
            formatted_news += f"   Search Engine: {article.get('search_engine', 'Unknown')}\n\n"
        
        return formatted_news
    
    def get_search_capabilities(self) -> Dict[str, bool]:
        """
        Check which search methods are available
        """
        capabilities = {
            'serper_api': bool(self.serper_api_key),
            'duckduckgo': False,
            'mock_data': True
        }
        
        # Check if DuckDuckGo is available
        try:
            from duckduckgo_search import DDGS
            capabilities['duckduckgo'] = True
        except ImportError:
            pass
        
        return capabilities