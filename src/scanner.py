import requests
from googlesearch import search
from serpapi import GoogleSearch
from fake_useragent import UserAgent
import time
import random
class TwitterScanner:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
    def scan_serpapi(self, query_username, api_key):
        """
        Uses SerpApi to find indexed profiles with high reliability.
        """
        if not api_key:
            return []
            
        results = []
        params = {
            "q": f'site:twitter.com "{query_username}" OR site:x.com "{query_username}"',
            "api_key": api_key,
            "num": 20
        }
        
        try:
            search = GoogleSearch(params)
            data = search.get_dict()
            organic_results = data.get("organic_results", [])
            
            for res in organic_results:
                link = res.get("link", "")
                title = res.get("title", "")
                if "status" not in link and "search" not in link:
                    results.append({
                        "username": query_username,
                        "url": link,
                        "title": title,
                        "method": "SerpApi"
                    })
        except Exception as e:
            # print(f"SerpApi Error: {e}") # Optional debug
            pass
            
        return results
    def scan_serp(self, query_username):
        """
        Uses Google Dorking to find indexed profiles.
        Search for: site:twitter.com "username" OR site:x.com "username"
        """
        results = []
        query = f'site:twitter.com "{query_username}" OR site:x.com "{query_username}"'
        
        try:
            # Fetch top 10 results
            for url in search(query, num_results=10, advanced=True):
                # Filter for actual profile links (simple heuristic)
                if "status" not in url.url and "search" not in url.url:
                    results.append({
                        "username": query_username,
                        "url": url.url,
                        "title": url.title,
                        "method": "SERP"
                    })
        except Exception as e:
            # Fail silently or log if needed, SERP can be flaky
            pass
            
        return results
    def verify_profile_direct(self, username):
        """
        Directly checks if x.com/{username} returns 200 OK and is ACTIVE (not suspended).
        """
        url = f"https://x.com/{username}"
        headers = {
            'User-Agent': self.ua.random,
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://google.com'
        }
        
        try:
            # Must use GET to see content for suspension check
            response = self.session.get(url, headers=headers, timeout=5, allow_redirects=True)
            
            if response.status_code == 200:
                # Basic 200 OK. Now check for suspension/restriction markers.
                # Note: X.com pages are heavy JS, but basic suspension text often appears in title or meta tags.
                # We look for common keywords in the raw HTML.
                text = response.text.lower()
                
                if "account suspended" in text or "account has been suspended" in text:
                    return None # Filter out (Suspended)
                
                if "caution: this account is temporarily restricted" in text:
                    return None # Filter out (Restricted)
                    
                # If we passed basic text checks, assume active enough to report
                return {
                    "username": username,
                    "url": url,
                    "status": "Active",
                    "method": "Direct"
                }
            elif response.status_code == 404:
                return None # Does not exist
            else:
                return None # Other errors (blocked/hidden)
                
        except Exception:
            return None
    def scan_candidates(self, candidates):
        """
        Orchestrator: checks a list of candidate usernames.
        """
        found = []
        for cand in candidates:
            # Sleep slightly to avoid instant IP ban
            time.sleep(random.uniform(0.5, 1.5)) 
            result = self.verify_profile_direct(cand)
            if result:
                found.append(result)
        return found
