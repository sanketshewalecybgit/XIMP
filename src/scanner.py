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
        Directly checks if x.com/{username} returns 200 OK.
        NOTE: This is rate-limited and liable to false positives due to login redirects.
        """
        url = f"https://x.com/{username}"
        headers = {
            'User-Agent': self.ua.random,
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://google.com'
        }
        
        try:
            # We use a HEAD request first to be lighter, fallback to GET
            response = self.session.get(url, headers=headers, timeout=5, allow_redirects=True)
            
            # X often redirects to /i/flow/login for some profiles or just returns 200 for the main skeleton
            # A 404 is a strong indicator it doesn't exist.
            if response.status_code == 200:
                return {
                    "username": username,
                    "url": url,
                    "status": "Active (Probed)",
                    "method": "Direct"
                }
            elif response.status_code == 404:
                return None # Does not exist
            else:
                return None # Other errors (429, 403) - assume hidden or blocked
                
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
